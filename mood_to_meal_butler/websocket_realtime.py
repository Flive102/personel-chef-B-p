"""
WebSocket Real-time Updates Module

Provides:
- Real-time health status updates
- Performance metrics streaming
- Alert notifications via WebSocket
- Client connection management
"""

from typing import Dict, List, Callable, Optional
from datetime import datetime
import json
import asyncio


class WebSocketManager:
    """Manage WebSocket connections for real-time updates."""
    
    def __init__(self):
        self.clients = []
        self.message_handlers = {}
        self.health_update_interval = 5  # seconds
        self.performance_update_interval = 10  # seconds
    
    def register_client(self, client_id: str) -> Dict:
        """Register a new WebSocket client."""
        client = {
            'id': client_id,
            'connected_at': datetime.now().isoformat(),
            'subscriptions': []
        }
        self.clients.append(client)
        return client
    
    def unregister_client(self, client_id: str) -> bool:
        """Unregister a WebSocket client."""
        self.clients = [c for c in self.clients if c['id'] != client_id]
        return True
    
    def subscribe_client(self, client_id: str, channel: str) -> Dict:
        """Subscribe client to update channel."""
        for client in self.clients:
            if client['id'] == client_id:
                if channel not in client['subscriptions']:
                    client['subscriptions'].append(channel)
                return {'status': 'subscribed', 'channel': channel}
        return {'error': 'Client not found'}
    
    def get_connected_clients(self) -> int:
        """Get count of connected clients."""
        return len(self.clients)
    
    def get_client_subscriptions(self, client_id: str) -> List[str]:
        """Get client subscriptions."""
        for client in self.clients:
            if client['id'] == client_id:
                return client['subscriptions']
        return []
    
    async def broadcast_health_status(self) -> Dict:
        """Broadcast health status to subscribers."""
        from mood_to_meal_butler.api_convenience import SystemStatus
        
        status = SystemStatus.get_health_check()
        
        return {
            'type': 'health_status',
            'timestamp': datetime.now().isoformat(),
            'data': status,
            'clients_subscribed': sum(
                1 for c in self.clients 
                if 'health' in c['subscriptions']
            )
        }
    
    async def broadcast_performance_metrics(self) -> Dict:
        """Broadcast performance metrics to subscribers."""
        from mood_to_meal_butler.api_convenience import PerformanceFacade
        
        metrics = PerformanceFacade.get_performance_baseline()
        
        return {
            'type': 'performance_metrics',
            'timestamp': datetime.now().isoformat(),
            'data': metrics,
            'clients_subscribed': sum(
                1 for c in self.clients 
                if 'performance' in c['subscriptions']
            )
        }
    
    async def broadcast_alert(self, alert_type: str, message: str, severity: str = 'warning') -> Dict:
        """Broadcast alert to subscribers."""
        alert = {
            'type': 'alert',
            'alert_type': alert_type,
            'message': message,
            'severity': severity,
            'timestamp': datetime.now().isoformat()
        }
        
        return {
            'alert': alert,
            'clients_subscribed': sum(
                1 for c in self.clients 
                if 'alerts' in c['subscriptions']
            )
        }
    
    async def stream_health_updates(self):
        """Stream health updates at interval."""
        while True:
            update = await self.broadcast_health_status()
            yield update
            await asyncio.sleep(self.health_update_interval)
    
    async def stream_performance_updates(self):
        """Stream performance updates at interval."""
        while True:
            update = await self.broadcast_performance_metrics()
            yield update
            await asyncio.sleep(self.performance_update_interval)


class WebSocketHandler:
    """WebSocket message handler."""
    
    def __init__(self):
        self.manager = WebSocketManager()
        self.message_routes = {
            'subscribe': self.handle_subscribe,
            'unsubscribe': self.handle_unsubscribe,
            'query_status': self.handle_query_status,
            'request_alert': self.handle_request_alert,
        }
    
    async def handle_message(self, client_id: str, message: Dict) -> Dict:
        """Handle incoming WebSocket message."""
        action = message.get('action')
        
        if action in self.message_routes:
            return await self.message_routes[action](client_id, message)
        
        return {'error': f'Unknown action: {action}'}
    
    async def handle_subscribe(self, client_id: str, message: Dict) -> Dict:
        """Handle subscribe message."""
        channel = message.get('channel')
        return self.manager.subscribe_client(client_id, channel)
    
    async def handle_unsubscribe(self, client_id: str, message: Dict) -> Dict:
        """Handle unsubscribe message."""
        channel = message.get('channel')
        subs = self.manager.get_client_subscriptions(client_id)
        if channel in subs:
            subs.remove(channel)
            return {'status': 'unsubscribed', 'channel': channel}
        return {'error': 'Not subscribed to channel'}
    
    async def handle_query_status(self, client_id: str, message: Dict) -> Dict:
        """Handle status query."""
        from mood_to_meal_butler.api_convenience import SystemStatus
        
        return SystemStatus.get_health_check()
    
    async def handle_request_alert(self, client_id: str, message: Dict) -> Dict:
        """Handle alert request."""
        alert_type = message.get('alert_type', 'system')
        return await self.manager.broadcast_alert(alert_type, 'Test alert')


# Global WebSocket manager instance
_ws_manager = None


def get_websocket_manager() -> WebSocketManager:
    """Get or create global WebSocket manager."""
    global _ws_manager
    if _ws_manager is None:
        _ws_manager = WebSocketManager()
    return _ws_manager


def get_websocket_handler() -> WebSocketHandler:
    """Get or create WebSocket handler."""
    return WebSocketHandler()
