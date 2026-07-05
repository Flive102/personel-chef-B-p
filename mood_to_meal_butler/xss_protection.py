"""
XSS Output Validation and HTML Escaping for mood-to-meal-butler
Prevents Cross-Site Scripting attacks through safe output encoding
"""

import html
import re
from typing import Any, Dict, List, Optional


class XSSProtection:
    """Prevent XSS attacks through output encoding and validation."""
    
    # Dangerous HTML tags that should never be in output
    DANGEROUS_TAGS = {
        'script', 'iframe', 'object', 'embed', 'applet',
        'meta', 'link', 'style', 'form', 'input', 'button'
    }
    
    # Dangerous attributes that can execute JavaScript
    DANGEROUS_ATTRS = {
        'onload', 'onerror', 'onclick', 'onmouseover',
        'onmouseout', 'onmousemove', 'onfocus', 'onblur',
        'onchange', 'onsubmit', 'onkeydown', 'onkeyup',
        'onkeypress', 'ondblclick', 'oncontextmenu',
        'onwheel', 'onscroll', 'ontouchstart', 'ontouchend'
    }
    
    @staticmethod
    def escape_html(text: str) -> str:
        """
        Escape HTML special characters safely.
        Converts: < > & " ' to safe entities
        
        Args:
            text: String to escape
        
        Returns:
            HTML-safe escaped string
        """
        if not isinstance(text, str):
            return str(text)
        
        return html.escape(text, quote=True)
    
    @staticmethod
    def escape_javascript(text: str) -> str:
        """
        Escape text for safe use in JavaScript strings.
        
        Args:
            text: String to escape for JavaScript
        
        Returns:
            JavaScript-safe escaped string
        """
        if not isinstance(text, str):
            return str(text)
        
        # Escape backslashes first
        text = text.replace('\\', '\\\\')
        # Escape quotes
        text = text.replace('"', '\\"')
        text = text.replace("'", "\\'")
        # Escape newlines
        text = text.replace('\n', '\\n')
        text = text.replace('\r', '\\r')
        
        return text
    
    @staticmethod
    def escape_url(url: str) -> str:
        """
        Escape URL to prevent XSS through href/src.
        
        Args:
            url: URL to escape
        
        Returns:
            Safe URL string
        """
        if not isinstance(url, str):
            return ""
        
        # Block javascript: protocol
        if url.lower().startswith('javascript:'):
            return ""
        
        # Block data: protocol with content type text/html
        if url.lower().startswith('data:text/html'):
            return ""
        
        # Escape special characters
        return html.escape(url, quote=True)
    
    @staticmethod
    def remove_html_tags(text: str) -> str:
        """
        Remove all HTML tags from text.
        
        Args:
            text: String that may contain HTML
        
        Returns:
            Text with HTML tags removed
        """
        if not isinstance(text, str):
            return str(text)
        
        # Remove all HTML tags
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)
    
    @staticmethod
    def validate_clean_html(html_content: str) -> bool:
        """
        Validate that HTML contains no dangerous tags or attributes.
        
        Args:
            html_content: HTML string to validate
        
        Returns:
            True if safe, False if dangerous content detected
        """
        if not isinstance(html_content, str):
            return False
        
        # Check for dangerous tags
        for tag in XSSProtection.DANGEROUS_TAGS:
            if re.search(rf'<{tag}[\s/>]', html_content, re.IGNORECASE):
                return False
        
        # Check for dangerous attributes
        for attr in XSSProtection.DANGEROUS_ATTRS:
            if re.search(rf'{attr}\s*=', html_content, re.IGNORECASE):
                return False
        
        # Check for javascript: protocol
        if 'javascript:' in html_content.lower():
            return False
        
        # Check for data: protocol with html
        if 'data:text/html' in html_content.lower():
            return False
        
        return True
    
    @staticmethod
    def sanitize_response(data: Any) -> Any:
        """
        Sanitize any data type for safe JSON response.
        
        Args:
            data: Data to sanitize (dict, list, str, etc.)
        
        Returns:
            Sanitized data safe for JSON output
        """
        if isinstance(data, dict):
            return {
                k: XSSProtection.sanitize_response(v)
                for k, v in data.items()
            }
        elif isinstance(data, list):
            return [XSSProtection.sanitize_response(item) for item in data]
        elif isinstance(data, str):
            return XSSProtection.escape_html(data)
        else:
            return data


def safe_format_response(template: str, **kwargs) -> str:
    """
    Safely format response with escaped variables.
    
    Usage:
        response = safe_format_response(
            "Hello {name}, your emotion is {emotion}",
            name="John",
            emotion="happy"
        )
    
    Args:
        template: Template string with {variable} placeholders
        **kwargs: Variables to insert (will be escaped)
    
    Returns:
        Formatted string with escaped variables
    """
    escaped_kwargs = {
        k: XSSProtection.escape_html(str(v))
        for k, v in kwargs.items()
    }
    
    return template.format(**escaped_kwargs)


def safe_concat(*strings: str, separator: str = "") -> str:
    """
    Safely concatenate strings with HTML escaping.
    
    Usage:
        result = safe_concat("Hello", " ", "World")
    
    Args:
        *strings: Strings to concatenate
        separator: String to join with
    
    Returns:
        Safely concatenated string
    """
    escaped = [XSSProtection.escape_html(str(s)) for s in strings]
    return separator.join(escaped)
