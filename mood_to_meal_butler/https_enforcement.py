"""
HTTPS Enforcement for mood-to-meal-butler
Enforces HTTPS connections and sets security headers
"""

from typing import Optional


class HTTPSEnforcement:
    """Enforce HTTPS and configure SSL/TLS security."""
    
    @staticmethod
    def get_https_headers() -> dict:
        """
        Get headers that enforce HTTPS.
        
        Returns:
            Dict of HTTPS enforcement headers
        """
        return {
            # Strict-Transport-Security: Force HTTPS for 1 year
            "Strict-Transport-Security": (
                "max-age=31536000; includeSubDomains; preload"
            ),
            
            # Upgrade insecure requests to HTTPS
            "Upgrade-Insecure-Requests": "1"
        }
    
    @staticmethod
    def attach_https_to_app(app, environment: str = "production"):
        """
        Attach HTTPS enforcement to Flask app.
        
        Usage:
            from flask import Flask
            from mood_to_meal_butler.https_enforcement import HTTPSEnforcement
            
            app = Flask(__name__)
            HTTPSEnforcement.attach_https_to_app(app)
        
        Args:
            app: Flask application instance
            environment: "production", "staging", or "development"
        """
        
        @app.before_request
        def redirect_to_https():
            """Redirect HTTP requests to HTTPS."""
            from flask import request, redirect
            
            # Skip in development
            if environment == "development":
                return
            
            # Skip if already HTTPS
            if request.url.startswith("https://"):
                return
            
            # Skip health check endpoints
            if request.path in ["/health", "/healthz", "/.well-known/acme-challenge"]:
                return
            
            # Redirect to HTTPS
            url = request.url.replace("http://", "https://", 1)
            return redirect(url, code=301)
        
        @app.after_request
        def add_https_headers(response):
            """Add HTTPS headers to response."""
            headers = HTTPSEnforcement.get_https_headers()
            
            for header, value in headers.items():
                response.headers[header] = value
            
            return response


class SSLConfiguration:
    """Configure SSL/TLS certificates."""
    
    @staticmethod
    def get_ssl_context_config() -> dict:
        """
        Get SSL context configuration.
        
        Returns:
            Dict with SSL configuration
        """
        return {
            "protocol": "TLSv1.2",
            "min_version": "TLSv1.2",
            "max_version": "TLSv1.3",
            "ciphers": (
                "ECDHE-ECDSA-AES128-GCM-SHA256:"
                "ECDHE-RSA-AES128-GCM-SHA256:"
                "ECDHE-ECDSA-AES256-GCM-SHA384:"
                "ECDHE-RSA-AES256-GCM-SHA384:"
                "DHE-RSA-AES128-GCM-SHA256:"
                "DHE-RSA-AES256-GCM-SHA384"
            ),
            "options": (
                "SSL_OP_NO_SSLv2 | "
                "SSL_OP_NO_SSLv3 | "
                "SSL_OP_NO_TLSv1 | "
                "SSL_OP_NO_TLSv1_1 | "
                "SSL_OP_NO_COMPRESSION | "
                "SSL_OP_CIPHER_SERVER_PREFERENCE"
            )
        }
    
    @staticmethod
    def generate_self_signed_cert_command() -> str:
        """
        Get command to generate self-signed certificate for development.
        
        Usage:
            # Run this command in terminal to generate dev certificates
            command = SSLConfiguration.generate_self_signed_cert_command()
            # Copy and run in shell
        
        Returns:
            Shell command to generate certificate
        """
        return (
            "openssl req -x509 -newkey rsa:4096 -nodes "
            "-out cert.pem -keyout key.pem -days 365 "
            "-subj '/C=US/ST=State/L=City/O=Org/CN=localhost'"
        )
    
    @staticmethod
    def get_production_ssl_config(cert_path: str, key_path: str) -> dict:
        """
        Get production SSL configuration.
        
        Args:
            cert_path: Path to SSL certificate file
            key_path: Path to SSL private key file
        
        Returns:
            Dict with production SSL config
        """
        return {
            "ssl_context": "adhoc",
            "cert": cert_path,
            "key": key_path,
            "protocols": ["TLSv1.2", "TLSv1.3"]
        }


def run_flask_with_https(app, 
                        host: str = "0.0.0.0",
                        port: int = 8443,
                        cert_path: Optional[str] = None,
                        key_path: Optional[str] = None,
                        environment: str = "production"):
    """
    Run Flask application with HTTPS.
    
    Usage - Development (self-signed):
        from mood_to_meal_butler.https_enforcement import run_flask_with_https
        run_flask_with_https(app, environment="development")
    
    Usage - Production:
        run_flask_with_https(
            app,
            cert_path="/etc/ssl/certs/cert.pem",
            key_path="/etc/ssl/private/key.pem",
            environment="production"
        )
    
    Args:
        app: Flask application
        host: Host to bind to
        port: Port to bind to
        cert_path: Path to SSL certificate
        key_path: Path to SSL private key
        environment: "production", "staging", or "development"
    """
    HTTPSEnforcement.attach_https_to_app(app, environment)
    
    if environment == "development":
        # Self-signed certificate for development
        app.run(
            host=host,
            port=port,
            ssl_context="adhoc",
            debug=True
        )
    else:
        # Production with certificates
        app.run(
            host=host,
            port=port,
            ssl_context=(cert_path, key_path),
            debug=False
        )
