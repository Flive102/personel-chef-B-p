"""
Advanced API Endpoints - HTTP Interface for System Operations

Provides REST endpoints for:
- Security checks
- Performance testing
- Compliance verification
- System status
- Data export

Compatible with FastAPI/Flask
"""

from typing import Dict, Optional
from datetime import datetime
import json


class APIEndpoints:
    """HTTP API endpoint handlers."""
    
    @staticmethod
    def security_check(vuln_type: Optional[str] = None) -> Dict:
        """
        GET /api/security
        GET /api/security?type=sql_injection
        
        Returns security audit or specific vulnerability check.
        """
        from mood_to_meal_butler.api_convenience import SecurityCheckFacade
        
        if vuln_type:
            data = SecurityCheckFacade.check_vulnerability(vuln_type)
        else:
            data = SecurityCheckFacade.quick_security_scan()
        
        return {
            'success': True,
            'data': data,
            'timestamp': datetime.now().isoformat()
        }
    
    @staticmethod
    def performance_test(scenario: str = 'light') -> Dict:
        """
        GET /api/performance
        GET /api/performance?scenario=medium
        
        Runs load test with specified scenario.
        """
        from mood_to_meal_butler.api_convenience import PerformanceFacade
        
        result = PerformanceFacade.quick_load_test(scenario)
        
        return {
            'success': True,
            'data': result,
            'timestamp': datetime.now().isoformat()
        }
    
    @staticmethod
    def compliance_check(framework: Optional[str] = None) -> Dict:
        """
        GET /api/compliance
        GET /api/compliance?framework=gdpr
        
        Returns compliance audit for all frameworks or specific one.
        """
        from mood_to_meal_butler.api_convenience import ComplianceFacade
        
        if framework:
            data = ComplianceFacade.check_compliance(framework)
        else:
            data = ComplianceFacade.check_all_compliance()
        
        return {
            'success': True,
            'data': data,
            'timestamp': datetime.now().isoformat()
        }
    
    @staticmethod
    def system_status(health_only: bool = False) -> Dict:
        """
        GET /api/status
        GET /api/status?health=true
        
        Returns full system status or quick health check.
        """
        from mood_to_meal_butler.api_convenience import SystemStatus
        
        if health_only:
            data = SystemStatus.get_health_check()
        else:
            data = SystemStatus.get_full_status()
        
        return {
            'success': True,
            'data': data,
            'timestamp': datetime.now().isoformat()
        }
    
    @staticmethod
    def cache_operations(action: str = 'status') -> Dict:
        """
        GET /api/cache?action=status
        POST /api/cache?action=clear
        
        Get cache status or clear caches.
        """
        from mood_to_meal_butler.api_convenience import CachingFacade
        
        if action == 'clear':
            data = CachingFacade.clear_caches()
        else:
            data = CachingFacade.get_cache_status()
        
        return {
            'success': True,
            'data': data,
            'timestamp': datetime.now().isoformat()
        }
    
    @staticmethod
    def database_status(pool_stats: bool = False) -> Dict:
        """
        GET /api/database
        GET /api/database?pool=true
        
        Get database status or connection pool stats.
        """
        from mood_to_meal_butler.api_convenience import DatabaseFacade
        
        if pool_stats:
            data = DatabaseFacade.pool_statistics()
        else:
            data = DatabaseFacade.get_db_status()
        
        return {
            'success': True,
            'data': data,
            'timestamp': datetime.now().isoformat()
        }


class FastAPISetup:
    """FastAPI route definitions (reference)."""
    
    @staticmethod
    def get_routes() -> str:
        """Get FastAPI route definitions as string."""
        return """
from fastapi import FastAPI, Query
from mood_to_meal_butler.api_endpoints import APIEndpoints

app = FastAPI(title="Mood-to-Meal Butler", version="1.0")

@app.get("/api/security")
async def get_security(type: str = Query(None)):
    return APIEndpoints.security_check(type)

@app.get("/api/performance")
async def get_performance(scenario: str = Query("light")):
    return APIEndpoints.performance_test(scenario)

@app.get("/api/compliance")
async def get_compliance(framework: str = Query(None)):
    return APIEndpoints.compliance_check(framework)

@app.get("/api/status")
async def get_status(health: bool = Query(False)):
    return APIEndpoints.system_status(health)

@app.get("/api/cache")
@app.post("/api/cache")
async def manage_cache(action: str = Query("status")):
    return APIEndpoints.cache_operations(action)

@app.get("/api/database")
async def get_database(pool: bool = Query(False)):
    return APIEndpoints.database_status(pool)

@app.get("/health")
async def health_check():
    return {"status": "ok"}
"""


class FlaskSetup:
    """Flask route definitions (reference)."""
    
    @staticmethod
    def get_routes() -> str:
        """Get Flask route definitions as string."""
        return """
from flask import Flask, request
from mood_to_meal_butler.api_endpoints import APIEndpoints

app = Flask(__name__)

@app.route("/api/security", methods=["GET"])
def security():
    vuln_type = request.args.get("type")
    return APIEndpoints.security_check(vuln_type)

@app.route("/api/performance", methods=["GET"])
def performance():
    scenario = request.args.get("scenario", "light")
    return APIEndpoints.performance_test(scenario)

@app.route("/api/compliance", methods=["GET"])
def compliance():
    framework = request.args.get("framework")
    return APIEndpoints.compliance_check(framework)

@app.route("/api/status", methods=["GET"])
def status():
    health = request.args.get("health", False)
    return APIEndpoints.system_status(health)

@app.route("/api/cache", methods=["GET", "POST"])
def cache():
    action = request.args.get("action", "status")
    return APIEndpoints.cache_operations(action)

@app.route("/api/database", methods=["GET"])
def database():
    pool = request.args.get("pool", False)
    return APIEndpoints.database_status(pool)

@app.route("/health", methods=["GET"])
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(debug=False, port=5000)
"""
