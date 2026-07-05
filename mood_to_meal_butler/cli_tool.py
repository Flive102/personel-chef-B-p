"""
CLI Tool - Command-line Interface for User Interaction

Provides simple CLI commands:
- security: Run security checks
- performance: Run load tests
- compliance: Check compliance
- status: Get system status
- export: Export data
- cache: Manage caching
- db: Database operations
"""

import argparse
import json
from typing import Dict, Optional
from datetime import datetime


class CLICommands:
    """Command handlers for CLI."""
    
    @staticmethod
    def handle_security(args) -> str:
        """Handle security command."""
        from mood_to_meal_butler.api_convenience import SecurityCheckFacade
        
        if args.vuln_type:
            result = SecurityCheckFacade.check_vulnerability(args.vuln_type)
        else:
            result = SecurityCheckFacade.quick_security_scan()
        
        return json.dumps(result, indent=2)
    
    @staticmethod
    def handle_performance(args) -> str:
        """Handle performance command."""
        from mood_to_meal_butler.api_convenience import PerformanceFacade
        
        if args.load_test:
            result = PerformanceFacade.quick_load_test(args.load_test)
        else:
            result = PerformanceFacade.get_performance_baseline()
        
        return json.dumps(result, indent=2)
    
    @staticmethod
    def handle_compliance(args) -> str:
        """Handle compliance command."""
        from mood_to_meal_butler.api_convenience import ComplianceFacade
        
        if args.framework:
            result = ComplianceFacade.check_compliance(args.framework)
        else:
            result = ComplianceFacade.check_all_compliance()
        
        return json.dumps(result, indent=2)
    
    @staticmethod
    def handle_status(args) -> str:
        """Handle status command."""
        from mood_to_meal_butler.api_convenience import SystemStatus
        
        if args.health:
            result = SystemStatus.get_health_check()
        else:
            result = SystemStatus.get_full_status()
        
        return json.dumps(result, indent=2)
    
    @staticmethod
    def handle_cache(args) -> str:
        """Handle cache command."""
        from mood_to_meal_butler.api_convenience import CachingFacade
        
        if args.clear:
            result = CachingFacade.clear_caches()
        else:
            result = CachingFacade.get_cache_status()
        
        return json.dumps(result, indent=2)
    
    @staticmethod
    def handle_db(args) -> str:
        """Handle database command."""
        from mood_to_meal_butler.api_convenience import DatabaseFacade
        
        if args.pool:
            result = DatabaseFacade.pool_statistics()
        else:
            result = DatabaseFacade.get_db_status()
        
        return json.dumps(result, indent=2)


def create_parser() -> argparse.ArgumentParser:
    """Create CLI argument parser."""
    parser = argparse.ArgumentParser(
        description='Mood-to-Meal Butler - Security & Performance CLI'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Security command
    security = subparsers.add_parser('security', help='Security checks')
    security.add_argument(
        '--vuln-type',
        choices=['sql_injection', 'xss', 'auth', 'dos'],
        help='Specific vulnerability to check'
    )
    
    # Performance command
    performance = subparsers.add_parser('performance', help='Performance tests')
    performance.add_argument(
        '--load-test',
        choices=['light', 'medium', 'heavy'],
        help='Load test scenario'
    )
    
    # Compliance command
    compliance = subparsers.add_parser('compliance', help='Compliance checks')
    compliance.add_argument(
        '--framework',
        choices=['gdpr', 'ccpa', 'hipaa'],
        help='Specific framework to check'
    )
    
    # Status command
    status = subparsers.add_parser('status', help='System status')
    status.add_argument('--health', action='store_true', help='Quick health check')
    
    # Cache command
    cache = subparsers.add_parser('cache', help='Cache management')
    cache.add_argument('--clear', action='store_true', help='Clear all caches')
    
    # Database command
    db = subparsers.add_parser('db', help='Database operations')
    db.add_argument('--pool', action='store_true', help='Show connection pool stats')
    
    return parser


def main():
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    handlers = {
        'security': CLICommands.handle_security,
        'performance': CLICommands.handle_performance,
        'compliance': CLICommands.handle_compliance,
        'status': CLICommands.handle_status,
        'cache': CLICommands.handle_cache,
        'db': CLICommands.handle_db,
    }
    
    if args.command in handlers:
        result = handlers[args.command](args)
        print(result)


if __name__ == '__main__':
    main()
