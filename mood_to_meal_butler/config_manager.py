"""
Configuration Manager - Centralized System Configuration

Manages:
- Security settings
- Performance tuning
- Compliance policies
- Caching configuration
- Database pooling
- Export defaults
"""

import json
import os
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class SecurityConfig:
    """Security configuration."""
    jwt_secret: str = "default-secret-key"
    rate_limit_per_minute: int = 60
    password_min_length: int = 8
    https_required: bool = True
    tls_version: str = "1.2"


@dataclass
class PerformanceConfig:
    """Performance tuning configuration."""
    cache_size: int = 10000
    cache_ttl_minutes: int = 60
    db_pool_size: int = 20
    db_pool_overflow: int = 40
    query_batch_size: int = 50
    load_test_concurrency: int = 100


@dataclass
class ComplianceConfig:
    """Compliance policy configuration."""
    gdpr_retention_days: int = 30
    ccpa_response_days: int = 45
    hipaa_audit_log_retention: int = 365
    sla_uptime_target: float = 99.9
    sla_response_time_ms: int = 200


@dataclass
class ExportConfig:
    """Export configuration defaults."""
    export_directory: str = "exports"
    json_indent: int = 2
    csv_encoding: str = "utf-8"
    html_theme: str = "default"


class ConfigurationManager:
    """Centralized configuration management."""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.security = SecurityConfig()
        self.performance = PerformanceConfig()
        self.compliance = ComplianceConfig()
        self.export = ExportConfig()
        self._load_config()
    
    def _load_config(self):
        """Load configuration from file if exists."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config_data = json.load(f)
                    self._apply_config(config_data)
            except Exception as e:
                print(f"Warning: Could not load config: {e}")
    
    def _apply_config(self, config_data: Dict):
        """Apply configuration from dict."""
        if 'security' in config_data:
            self.security = SecurityConfig(**config_data['security'])
        if 'performance' in config_data:
            self.performance = PerformanceConfig(**config_data['performance'])
        if 'compliance' in config_data:
            self.compliance = ComplianceConfig(**config_data['compliance'])
        if 'export' in config_data:
            self.export = ExportConfig(**config_data['export'])
    
    def save_config(self, filename: Optional[str] = None):
        """Save current configuration to file."""
        target = filename or self.config_file
        
        config_data = {
            'security': asdict(self.security),
            'performance': asdict(self.performance),
            'compliance': asdict(self.compliance),
            'export': asdict(self.export),
        }
        
        with open(target, 'w') as f:
            json.dump(config_data, f, indent=2)
    
    def get_security_config(self) -> Dict:
        """Get security settings."""
        return asdict(self.security)
    
    def update_security_config(self, **kwargs):
        """Update security settings."""
        for key, value in kwargs.items():
            if hasattr(self.security, key):
                setattr(self.security, key, value)
    
    def get_performance_config(self) -> Dict:
        """Get performance settings."""
        return asdict(self.performance)
    
    def update_performance_config(self, **kwargs):
        """Update performance settings."""
        for key, value in kwargs.items():
            if hasattr(self.performance, key):
                setattr(self.performance, key, value)
    
    def get_compliance_config(self) -> Dict:
        """Get compliance settings."""
        return asdict(self.compliance)
    
    def update_compliance_config(self, **kwargs):
        """Update compliance settings."""
        for key, value in kwargs.items():
            if hasattr(self.compliance, key):
                setattr(self.compliance, key, value)
    
    def get_export_config(self) -> Dict:
        """Get export settings."""
        return asdict(self.export)
    
    def update_export_config(self, **kwargs):
        """Update export settings."""
        for key, value in kwargs.items():
            if hasattr(self.export, key):
                setattr(self.export, key, value)
    
    def get_all_config(self) -> Dict:
        """Get all configuration."""
        return {
            'security': asdict(self.security),
            'performance': asdict(self.performance),
            'compliance': asdict(self.compliance),
            'export': asdict(self.export),
        }
    
    def generate_config_template(self, filename: str = "config.template.json"):
        """Generate configuration template file."""
        template = self.get_all_config()
        
        with open(filename, 'w') as f:
            json.dump(template, f, indent=2)
        
        return filename
    
    def validate_config(self) -> Dict:
        """Validate configuration values."""
        issues = []
        
        if self.security.password_min_length < 6:
            issues.append("password_min_length must be at least 6")
        
        if self.performance.cache_size < 100:
            issues.append("cache_size should be at least 100")
        
        if self.compliance.sla_uptime_target > 100 or self.compliance.sla_uptime_target < 0:
            issues.append("sla_uptime_target must be between 0-100")
        
        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'timestamp': __import__('datetime').datetime.now().isoformat()
        }


# Global configuration instance
_config_manager = None


def get_config() -> ConfigurationManager:
    """Get or create global configuration manager."""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigurationManager()
    return _config_manager


def reset_config():
    """Reset configuration (for testing)."""
    global _config_manager
    _config_manager = None
