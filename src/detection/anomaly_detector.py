import logging
from datetime import datetime, timedelta
from collections import deque

logger = logging.getLogger(__name__)

class AnomalyDetector:
    """
    Jalur B: Deteksi anomali berdasarkan CPU spike + suspicious login correlation
    """
    def __init__(self, cpu_spike_threshold: int = 30, window_seconds: int = 60):
        """
        Args:
            cpu_spike_threshold: % above baseline untuk trigger (default: 30%)
            window_seconds: Durasi window untuk baseline calculation (default: 60s)
        """
        self.cpu_spike_threshold = cpu_spike_threshold
        self.window_seconds = window_seconds
        
        # Buffer untuk tracking CPU & events
        self.cpu_buffer = deque(maxlen=60)  # 60 detik sampling
        self.baseline_cpu = None
        self.suspicious_ips = {}  # {ip: suspicion_score}
        
    def add_cpu_sample(self, cpu_percent: float, timestamp: datetime = None):
        """
        Add CPU sample ke buffer untuk baseline tracking
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        self.cpu_buffer.append((timestamp, cpu_percent))
        
        # Update baseline (average dari last 60 sec)
        if len(self.cpu_buffer) > 0:
            total_cpu = sum(cpu for _, cpu in self.cpu_buffer)
            self.baseline_cpu = total_cpu / len(self.cpu_buffer)
    
    def process_login_event(self, event, current_cpu: float) -> bool:
        """
        Process login event, check untuk anomaly (CPU spike + login correlation)
        
        Args:
            event: LoginEvent object (source_ip, result, etc)
            current_cpu: Current CPU % dari router
        
        Returns:
            Boolean: True jika ANOMALY detected
        """
        if self.baseline_cpu is None:
            logger.warning("⚠️ Baseline CPU not yet established, skipping anomaly check")
            return False
        
        # Calculate CPU spike
        cpu_increase_percent = ((current_cpu - self.baseline_cpu) / self.baseline_cpu) * 100
        
        # Check untuk CPU spike > threshold
        if cpu_increase_percent > self.cpu_spike_threshold:
            logger.debug(f"🔴 CPU spike detected: {cpu_increase_percent:.1f}% (baseline: {self.baseline_cpu:.1f}%, current: {current_cpu:.1f}%)")
            
            # Jika ada successful login saat spike → HIGH SUSPICION
            if event.result == 'success':
                ip = event.source_ip
                self.suspicious_ips[ip] = self.suspicious_ips.get(ip, 0) + 0.5
                logger.warning(f"⚠️ SUSPICIOUS: Successful login dari {ip} saat CPU spike!")
                
                if self.suspicious_ips[ip] >= 0.7:
                    logger.warning(f"🚨 ANOMALY DETECTED: {ip} (score: {self.suspicious_ips[ip]:.2f})")
                    return True
        
        # Jika banyak failed login + CPU normal = brute force (handled by Jalur A)
        # Anomaly Detector fokus ke: suspicious spike + successful login correlation
        
        return False
    
    def get_baseline(self) -> float:
        """Get current baseline CPU"""
        return self.baseline_cpu or 0.0
    
    def reset_suspicious(self, ip: str):
        """Reset suspicion score untuk IP"""
        if ip in self.suspicious_ips:
            del self.suspicious_ips[ip]
            logger.debug(f"✓ Reset suspicion score untuk {ip}")


# Test
if __name__ == "__main__":
    from src.parser.log_parser import LoginEvent
    
    detector = AnomalyDetector(cpu_spike_threshold=30)
    
    # Simulate baseline: normal CPU 12%
    for i in range(60):
        detector.add_cpu_sample(12.0)
    
    print(f"Baseline CPU: {detector.get_baseline():.1f}%")
    
    # Simulate attack: CPU spike 50%
    event = LoginEvent(
        timestamp=datetime.now(),
        source_ip="192.168.20.2",
        username="admin",
        service="ssh",
        result="success"
    )
    
    is_anomaly = detector.process_login_event(event, current_cpu=50.0)
    print(f"Anomaly detected: {is_anomaly}")