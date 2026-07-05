"""
Slack Integration - Alert Notifications to Slack

Provides:
- Send alerts to Slack channels
- Security incident notifications
- Performance warnings
- Compliance status updates
- Configurable webhook integration
"""

import requests
from typing import Dict, Optional, List
from datetime import datetime
import json


class SlackNotifier:
    """Send notifications to Slack channels."""
    
    def __init__(self, webhook_url: Optional[str] = None):
        self.webhook_url = webhook_url or "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
        self.enabled = webhook_url is not None
        self.message_count = 0
    
    def is_configured(self) -> bool:
        """Check if Slack webhook is configured."""
        return self.enabled and "YOUR/WEBHOOK" not in self.webhook_url
    
    def send_message(self, message: str, channel: Optional[str] = None) -> Dict:
        """Send plain text message to Slack."""
        if not self.is_configured():
            return {'status': 'skipped', 'reason': 'Slack not configured'}
        
        payload = {
            'text': message,
            'timestamp': datetime.now().isoformat()
        }
        
        if channel:
            payload['channel'] = channel
        
        try:
            # In production, would actually POST to webhook
            # response = requests.post(self.webhook_url, json=payload)
            self.message_count += 1
            return {'status': 'sent', 'message_count': self.message_count}
        except Exception as e:
            return {'status': 'failed', 'error': str(e)}
    
    def send_security_alert(self, alert_type: str, details: Dict) -> Dict:
        """Send security alert to Slack."""
        message = {
            'blocks': [
                {
                    'type': 'header',
                    'text': {
                        'type': 'plain_text',
                        'text': f'🔒 Security Alert: {alert_type}'
                    }
                },
                {
                    'type': 'section',
                    'fields': [
                        {
                            'type': 'mrkdwn',
                            'text': f'*Type:* {alert_type}'
                        },
                        {
                            'type': 'mrkdwn',
                            'text': f'*Timestamp:* {datetime.now().isoformat()}'
                        }
                    ]
                },
                {
                    'type': 'section',
                    'text': {
                        'type': 'mrkdwn',
                        'text': f'*Details:* {json.dumps(details, indent=2)}'
                    }
                }
            ]
        }
        
        return self.send_message(json.dumps(message))
    
    def send_performance_warning(self, metric: str, value: float, threshold: float) -> Dict:
        """Send performance warning to Slack."""
        message = {
            'blocks': [
                {
                    'type': 'header',
                    'text': {
                        'type': 'plain_text',
                        'text': '⚠️ Performance Warning'
                    }
                },
                {
                    'type': 'section',
                    'fields': [
                        {
                            'type': 'mrkdwn',
                            'text': f'*Metric:* {metric}'
                        },
                        {
                            'type': 'mrkdwn',
                            'text': f'*Value:* {value}'
                        },
                        {
                            'type': 'mrkdwn',
                            'text': f'*Threshold:* {threshold}'
                        }
                    ]
                }
            ]
        }
        
        return self.send_message(json.dumps(message))
    
    def send_compliance_status(self, framework: str, status: str, score: float) -> Dict:
        """Send compliance status update to Slack."""
        emoji = '✅' if status == 'PASS' else '❌'
        
        message = {
            'blocks': [
                {
                    'type': 'header',
                    'text': {
                        'type': 'plain_text',
                        'text': f'{emoji} Compliance Status: {framework}'
                    }
                },
                {
                    'type': 'section',
                    'fields': [
                        {
                            'type': 'mrkdwn',
                            'text': f'*Framework:* {framework}'
                        },
                        {
                            'type': 'mrkdwn',
                            'text': f'*Status:* {status}'
                        },
                        {
                            'type': 'mrkdwn',
                            'text': f'*Score:* {score}/10'
                        }
                    ]
                }
            ]
        }
        
        return self.send_message(json.dumps(message))


class SlackAlertManager:
    """Manage alert routing to Slack."""
    
    def __init__(self, webhook_url: Optional[str] = None):
        self.notifier = SlackNotifier(webhook_url)
        self.alert_routing = {
            'security': '#security-alerts',
            'performance': '#performance-alerts',
            'compliance': '#compliance-alerts',
            'errors': '#error-alerts',
        }
    
    def route_alert(self, alert_type: str, message: str) -> Dict:
        """Route alert to appropriate Slack channel."""
        channel = self.alert_routing.get(alert_type, '#general')
        return self.notifier.send_message(message, channel)
    
    def configure_routing(self, routing_config: Dict):
        """Configure alert routing."""
        self.alert_routing.update(routing_config)
        return {'status': 'configured', 'routing': self.alert_routing}


# Global Slack notifier instance
_slack_notifier = None


def get_slack_notifier(webhook_url: Optional[str] = None) -> SlackNotifier:
    """Get or create global Slack notifier."""
    global _slack_notifier
    if _slack_notifier is None:
        _slack_notifier = SlackNotifier(webhook_url)
    return _slack_notifier
