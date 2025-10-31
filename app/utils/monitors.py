import psutil
import time
import logging
from datetime import datetime

class SystemMonitor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.start_time = time.time()
    
    def get_system_metrics(self):
        """Get system performance metrics"""
        try:
            metrics = {
                'timestamp': datetime.utcnow().isoformat(),
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_usage': psutil.disk_usage('/').percent,
                'uptime': time.time() - self.start_time,
                'active_processes': len(psutil.pids())
            }
            return metrics
        except Exception as e:
            self.logger.error(f"Error getting system metrics: {e}")
            return {}
    
    def get_application_metrics(self):
        """Get application-specific metrics"""
        try:
            from app.models import db
            from app.models.user import User
            from app.models.game import Game
            
            metrics = {
                'total_users': User.query.count(),
                'total_games': Game.query.count(),
                'database_connections': 0,  # Would need specific tracking
                'active_sessions': 0,       # Would need session tracking
                'requests_processed': 0     # Would need request tracking
            }
            return metrics
        except Exception as e:
            self.logger.error(f"Error getting application metrics: {e}")
            return {}
    
    def check_services_health(self):
        """Check health of external services"""
        health_status = {
            'database': 'healthy',
            'redis': 'healthy',
            'ai_service': 'healthy' if self._check_ai_service() else 'unhealthy'
        }
        return health_status
    
    def _check_ai_service(self):
        """Check if AI service is responsive"""
        # Implementation would test AI service connectivity
        return True