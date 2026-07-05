"""
XSS (Cross-Site Scripting) Security Tests for mood-to-meal-butler
Tests output encoding, HTML escaping, and payload sanitization
"""

import pytest
from mood_to_meal_butler.xss_protection import (
    XSSProtection, safe_format_response, safe_concat
)


class TestHTMLEscaping:
    """Test HTML character escaping."""
    
    def test_escape_less_than_symbol(self):
        """Test < is escaped to &lt;"""
        result = XSSProtection.escape_html("<")
        assert result == "&lt;"
    
    def test_escape_greater_than_symbol(self):
        """Test > is escaped to &gt;"""
        result = XSSProtection.escape_html(">")
        assert result == "&gt;"
    
    def test_escape_ampersand(self):
        """Test & is escaped to &amp;"""
        result = XSSProtection.escape_html("&")
        assert result == "&amp;"
    
    def test_escape_double_quote(self):
        """Test \" is escaped to &quot;"""
        result = XSSProtection.escape_html('"')
        assert result == "&quot;"
    
    def test_escape_script_tag(self):
        """Test <script> tag is escaped."""
        dangerous = "<script>alert('xss')</script>"
        result = XSSProtection.escape_html(dangerous)
        assert "<script>" not in result
        assert "&lt;script&gt;" in result


class TestJavaScriptEscaping:
    """Test JavaScript string escaping."""
    
    def test_escape_single_quote(self):
        """Test single quote escaped for JavaScript."""
        result = XSSProtection.escape_javascript("it's")
        assert "\\'" in result or "\\\\" in result
    
    def test_escape_double_quote(self):
        """Test double quote escaped for JavaScript."""
        result = XSSProtection.escape_javascript('say "hello"')
        assert '\\"' in result
    
    def test_escape_newline(self):
        """Test newline escaped for JavaScript."""
        result = XSSProtection.escape_javascript("line1\nline2")
        assert "\\n" in result
    
    def test_escape_backslash(self):
        """Test backslash escaped for JavaScript."""
        result = XSSProtection.escape_javascript("path\\to\\file")
        assert "\\\\" in result


class TestURLEscaping:
    """Test URL escaping to prevent XSS."""
    
    def test_javascript_protocol_blocked(self):
        """Test javascript: protocol URLs are blocked."""
        dangerous_url = "javascript:alert('xss')"
        result = XSSProtection.escape_url(dangerous_url)
        assert result == ""
    
    def test_data_html_protocol_blocked(self):
        """Test data:text/html protocol is blocked."""
        dangerous_url = "data:text/html,<script>alert('xss')</script>"
        result = XSSProtection.escape_url(dangerous_url)
        assert result == ""
    
    def test_safe_url_preserved(self):
        """Test safe URLs are preserved."""
        safe_url = "https://example.com/page?id=123"
        result = XSSProtection.escape_url(safe_url)
        assert "https://example.com" in result


class TestHTMLTagRemoval:
    """Test HTML tag removal."""
    
    def test_remove_script_tags(self):
        """Test <script> tags removed."""
        html = "<p>Hello</p><script>alert('xss')</script>"
        result = XSSProtection.remove_html_tags(html)
        assert "<script>" not in result
        assert "Hello" in result
    
    def test_remove_img_tags(self):
        """Test <img> tags removed."""
        html = '<p>Text</p><img src=x onerror="alert()">'
        result = XSSProtection.remove_html_tags(html)
        assert "<img" not in result
        assert "Text" in result
    
    def test_remove_all_tags(self):
        """Test all HTML tags removed."""
        html = "<html><body><h1>Title</h1></body></html>"
        result = XSSProtection.remove_html_tags(html)
        assert "<" not in result
        assert ">" not in result


class TestDangerousTagDetection:
    """Test detection of dangerous HTML content."""
    
    def test_script_tag_detected(self):
        """Test <script> tag detection."""
        dangerous_html = "<script>alert('xss')</script>"
        is_safe = XSSProtection.validate_clean_html(dangerous_html)
        assert not is_safe
    
    def test_iframe_detected(self):
        """Test <iframe> tag detection."""
        dangerous_html = '<iframe src="http://evil.com"></iframe>'
        is_safe = XSSProtection.validate_clean_html(dangerous_html)
        assert not is_safe
    
    def test_event_handler_detected(self):
        """Test onclick event handler detection."""
        dangerous_html = '<img src=x onclick="alert(\'xss\')">'
        is_safe = XSSProtection.validate_clean_html(dangerous_html)
        assert not is_safe
    
    def test_safe_html_accepted(self):
        """Test safe HTML is accepted."""
        safe_html = "<p>This is safe text</p><b>Bold text</b>"
        is_safe = XSSProtection.validate_clean_html(safe_html)
        assert is_safe


class TestResponseSanitization:
    """Test sanitization of API responses."""
    
    def test_sanitize_string_response(self):
        """Test string response is escaped."""
        data = "<script>alert('xss')</script>"
        result = XSSProtection.sanitize_response(data)
        assert "<script>" not in result
        assert "&lt;script&gt;" in result
    
    def test_sanitize_dict_response(self):
        """Test dict response keys/values escaped."""
        data = {"message": "<img src=x onerror='alert()'>"}
        result = XSSProtection.sanitize_response(data)
        assert "&lt;img" in result["message"]
    
    def test_sanitize_list_response(self):
        """Test list response items escaped."""
        data = ["<script>", "safe text", "<iframe>"]
        result = XSSProtection.sanitize_response(data)
        assert all("&lt;" in str(item) or item == "safe text" for item in result)
    
    def test_sanitize_nested_structure(self):
        """Test nested structures sanitized."""
        data = {
            "user": {
                "name": "<script>alert('xss')</script>",
                "emotions": ["<img src=x>", "happy"]
            }
        }
        result = XSSProtection.sanitize_response(data)
        assert "&lt;script&gt;" in result["user"]["name"]
        assert "&lt;img" in result["user"]["emotions"][0]


class TestSafeFormatting:
    """Test safe string formatting utilities."""
    
    def test_safe_format_basic(self):
        """Test safe_format_response escapes variables."""
        result = safe_format_response(
            "Hello {name}",
            name="<script>alert('xss')</script>"
        )
        assert "<script>" not in result
        assert "&lt;script&gt;" in result
    
    def test_safe_concat_escapes(self):
        """Test safe_concat escapes all strings."""
        result = safe_concat(
            "Start",
            "<img src=x>",
            "End"
        )
        assert "<img" not in result
        assert "&lt;img" in result
