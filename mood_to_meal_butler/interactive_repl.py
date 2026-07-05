"""
Interactive Testing REPL - Real-time Feature Verification

Allows users to:
- Test security features
- Run performance checks
- Query compliance status
- Interact with system live
"""

import cmd
import json
from typing import Optional


class InteractiveREPL(cmd.Cmd):
    """Interactive command-line REPL for system testing."""
    
    intro = """
    ╔════════════════════════════════════════════════════════════════╗
    ║  Mood-to-Meal Butler - Interactive Testing Console            ║
    ║  Type 'help' for available commands                           ║
    ║  Type 'quit' or 'exit' to leave                              ║
    ╚════════════════════════════════════════════════════════════════╝
    """
    
    prompt = "butler> "
    
    def do_security(self, arg):
        """security [vuln_type] - Run security checks
        
        vuln_type options: sql_injection, xss, auth, dos
        Example: security sql_injection
        """
        from mood_to_meal_butler.api_convenience import SecurityCheckFacade
        
        if arg:
            result = SecurityCheckFacade.check_vulnerability(arg.strip())
        else:
            result = SecurityCheckFacade.quick_security_scan()
        
        print(json.dumps(result, indent=2))
    
    def do_performance(self, arg):
        """performance [scenario] - Run performance tests
        
        scenario options: light, medium, heavy
        Example: performance light
        """
        from mood_to_meal_butler.api_convenience import PerformanceFacade
        
        if arg:
            result = PerformanceFacade.quick_load_test(arg.strip())
        else:
            result = PerformanceFacade.get_performance_baseline()
        
        print(json.dumps(result, indent=2))
    
    def do_compliance(self, arg):
        """compliance [framework] - Check compliance status
        
        framework options: gdpr, ccpa, hipaa
        Example: compliance gdpr
        """
        from mood_to_meal_butler.api_convenience import ComplianceFacade
        
        if arg:
            result = ComplianceFacade.check_compliance(arg.strip())
        else:
            result = ComplianceFacade.check_all_compliance()
        
        print(json.dumps(result, indent=2))
    
    def do_status(self, arg):
        """status [--health] - Get system status
        
        --health flag shows quick health check only
        Example: status --health
        """
        from mood_to_meal_butler.api_convenience import SystemStatus
        
        if arg == '--health':
            result = SystemStatus.get_health_check()
        else:
            result = SystemStatus.get_full_status()
        
        print(json.dumps(result, indent=2))
    
    def do_cache(self, arg):
        """cache [--clear] - Manage cache
        
        --clear flag clears all caches
        Example: cache --clear
        """
        from mood_to_meal_butler.api_convenience import CachingFacade
        
        if arg == '--clear':
            result = CachingFacade.clear_caches()
        else:
            result = CachingFacade.get_cache_status()
        
        print(json.dumps(result, indent=2))
    
    def do_db(self, arg):
        """db [--pool] - Database operations
        
        --pool flag shows connection pool stats
        Example: db --pool
        """
        from mood_to_meal_butler.api_convenience import DatabaseFacade
        
        if arg == '--pool':
            result = DatabaseFacade.pool_statistics()
        else:
            result = DatabaseFacade.get_db_status()
        
        print(json.dumps(result, indent=2))
    
    def do_export(self, arg):
        """export [type] - Export system data
        
        type options: security, compliance, performance, all
        Example: export security
        """
        from mood_to_meal_butler.data_export import DataExporter
        
        if arg == 'all':
            files = DataExporter.export_system_report()
            print(f"✓ Exported {len(files)} files:")
            for key, path in files.items():
                print(f"  - {key}: {path}")
        elif arg == 'security':
            filename = DataExporter.export_security_audit()
            print(f"✓ Exported: {filename}")
        elif arg == 'compliance':
            filename = DataExporter.export_compliance_audit()
            print(f"✓ Exported: {filename}")
        elif arg == 'performance':
            filename = DataExporter.export_performance_metrics()
            print(f"✓ Exported: {filename}")
        else:
            print("Unknown export type. Use: security, compliance, performance, or all")
    
    def do_help(self, arg):
        """help [command] - Show help"""
        super().do_help(arg)
    
    def do_quit(self, arg):
        """quit - Exit the REPL"""
        print("Goodbye!")
        return True
    
    def do_exit(self, arg):
        """exit - Exit the REPL"""
        return self.do_quit(arg)
    
    def emptyline(self):
        """Do nothing on empty line"""
        pass


def run_repl():
    """Run interactive REPL."""
    repl = InteractiveREPL()
    repl.cmdloop()


if __name__ == '__main__':
    run_repl()
