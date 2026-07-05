"""
Batch Operations - Automate Common Tasks

Supports:
- Batch security audits
- Bulk performance tests
- Mass compliance checks
- Bulk data export
- Scheduled batch jobs
"""

import time
from typing import Dict, List, Callable, Any
from datetime import datetime


class BatchOperations:
    """Batch operation orchestration."""
    
    def __init__(self):
        self.results = []
        self.start_time = None
        self.end_time = None
    
    def batch_security_audits(self, vulnerability_types: List[str]) -> Dict:
        """Run security audits for multiple vulnerability types."""
        from mood_to_meal_butler.api_convenience import SecurityCheckFacade
        
        self.start_time = datetime.now()
        results = []
        
        for vuln_type in vulnerability_types:
            try:
                result = SecurityCheckFacade.check_vulnerability(vuln_type)
                results.append({
                    'vulnerability': vuln_type,
                    'result': result,
                    'status': 'SUCCESS'
                })
            except Exception as e:
                results.append({
                    'vulnerability': vuln_type,
                    'error': str(e),
                    'status': 'FAILED'
                })
        
        self.end_time = datetime.now()
        
        return {
            'operation': 'batch_security_audits',
            'total': len(vulnerability_types),
            'successful': sum(1 for r in results if r['status'] == 'SUCCESS'),
            'failed': sum(1 for r in results if r['status'] == 'FAILED'),
            'results': results,
            'duration_seconds': (self.end_time - self.start_time).total_seconds()
        }
    
    def batch_compliance_checks(self, frameworks: List[str]) -> Dict:
        """Run compliance checks for multiple frameworks."""
        from mood_to_meal_butler.api_convenience import ComplianceFacade
        
        self.start_time = datetime.now()
        results = []
        
        for framework in frameworks:
            try:
                result = ComplianceFacade.check_compliance(framework)
                results.append({
                    'framework': framework,
                    'result': result,
                    'status': 'SUCCESS'
                })
            except Exception as e:
                results.append({
                    'framework': framework,
                    'error': str(e),
                    'status': 'FAILED'
                })
        
        self.end_time = datetime.now()
        
        return {
            'operation': 'batch_compliance_checks',
            'total': len(frameworks),
            'successful': sum(1 for r in results if r['status'] == 'SUCCESS'),
            'failed': sum(1 for r in results if r['status'] == 'FAILED'),
            'results': results,
            'duration_seconds': (self.end_time - self.start_time).total_seconds()
        }
    
    def batch_performance_tests(self, scenarios: List[str]) -> Dict:
        """Run performance tests for multiple scenarios."""
        from mood_to_meal_butler.api_convenience import PerformanceFacade
        
        self.start_time = datetime.now()
        results = []
        
        for scenario in scenarios:
            try:
                result = PerformanceFacade.quick_load_test(scenario)
                results.append({
                    'scenario': scenario,
                    'result': result,
                    'status': 'SUCCESS'
                })
            except Exception as e:
                results.append({
                    'scenario': scenario,
                    'error': str(e),
                    'status': 'FAILED'
                })
        
        self.end_time = datetime.now()
        
        return {
            'operation': 'batch_performance_tests',
            'total': len(scenarios),
            'successful': sum(1 for r in results if r['status'] == 'SUCCESS'),
            'failed': sum(1 for r in results if r['status'] == 'FAILED'),
            'results': results,
            'duration_seconds': (self.end_time - self.start_time).total_seconds()
        }
    
    def batch_export_data(self, export_types: List[str]) -> Dict:
        """Export data in multiple formats."""
        from mood_to_meal_butler.data_export import DataExporter, ReportGenerator
        
        self.start_time = datetime.now()
        files = {}
        
        export_funcs = {
            'security': DataExporter.export_security_audit,
            'compliance': DataExporter.export_compliance_audit,
            'performance': DataExporter.export_performance_metrics,
            'cache': DataExporter.export_cache_status,
            'html_report': ReportGenerator.generate_html_summary,
            'text_report': ReportGenerator.generate_text_report,
        }
        
        for export_type in export_types:
            if export_type in export_funcs:
                try:
                    filename = export_funcs[export_type]()
                    files[export_type] = filename
                except Exception as e:
                    files[export_type] = f"Error: {str(e)}"
        
        self.end_time = datetime.now()
        
        return {
            'operation': 'batch_export_data',
            'total': len(export_types),
            'exports': files,
            'duration_seconds': (self.end_time - self.start_time).total_seconds()
        }
    
    def batch_full_audit(self) -> Dict:
        """Run complete system audit (security + compliance + performance)."""
        return {
            'security': self.batch_security_audits(['sql_injection', 'xss', 'auth', 'dos']),
            'compliance': self.batch_compliance_checks(['gdpr', 'ccpa', 'hipaa']),
            'performance': self.batch_performance_tests(['light', 'medium']),
            'timestamp': datetime.now().isoformat()
        }


# Global batch operations instance
_batch_ops = None


def get_batch_operations() -> BatchOperations:
    """Get or create global batch operations instance."""
    global _batch_ops
    if _batch_ops is None:
        _batch_ops = BatchOperations()
    return _batch_ops
