from collections import defaultdict
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class BruteForceDetector:
    def __init__(self, threshold: int = 10, window_seconds: int = 60):
        self.threshold = threshold
        self.window_seconds = window_seconds
        # Buffer: {source_ip: [timestamp1, timestamp2, ...]}
        self.failed_attempts = defaultdict(list)
    
    def process_event(self, event) -> bool:
        """
        Process login event, return True if THREAT detected
        """
        if event.result == 'failure':
            # Add to buffer
            self.failed_attempts[event.source_ip].append(event.timestamp)
            
            # Clean old entries (older than window)
            cutoff_time = event.timestamp - timedelta(seconds=self.window_seconds)
            self.failed_attempts[event.source_ip] = [
                ts for ts in self.failed_attempts[event.source_ip]
                if ts > cutoff_time
            ]
            
            # Check threshold
            count = len(self.failed_attempts[event.source_ip])
            if count >= self.threshold:
                logger.warning(f"🚨 BRUTE FORCE DETECTED: {event.source_ip} ({count} failures in {self.window_seconds}s)")
                return True
        
        return False
    
    def get_failed_count(self, source_ip: str) -> int:
        """Get current failed count for IP"""
        now = datetime.now()
        cutoff_time = now - timedelta(seconds=self.window_seconds)
        
        self.failed_attempts[source_ip] = [
            ts for ts in self.failed_attempts[source_ip]
            if ts > cutoff_time
        ]
        
        return len(self.failed_attempts[source_ip])