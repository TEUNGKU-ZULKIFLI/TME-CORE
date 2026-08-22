import time
from typing import Dict, Any, Optional

class DetectorJalurA:
    def __init__(self, whitelist_ips: list, max_failed_attempts: int = 5, time_window_seconds: int = 60):
        self.whitelist_ips = whitelist_ips
        self.max_failed_attempts = max_failed_attempts
        self.time_window_seconds = time_window_seconds

    def analyze_log(self, parsed_log: Dict[str, Any], failed_attempts: Dict[str, list], persistent_failed_counts: Dict[str, dict] = None) -> Optional[Dict[str, Any]]:
        if not parsed_log or parsed_log.get('status') != 'FAILED':
            return None

        ip = parsed_log.get('ip')
        service = parsed_log.get('service', 'unknown')
        username = parsed_log.get('username', 'unknown')

        if not ip or ip in self.whitelist_ips:
            return None

        now = time.time()

        if ip not in failed_attempts:
            failed_attempts[ip] = []

        failed_attempts[ip] = [ts for ts in failed_attempts[ip] if (now - ts) <= self.time_window_seconds]
        failed_attempts[ip].append(now)

        if persistent_failed_counts and ip in persistent_failed_counts:
            total_attempts = persistent_failed_counts[ip].get('count', len(failed_attempts[ip]))
        else:
            total_attempts = len(failed_attempts[ip])

        if total_attempts >= self.max_failed_attempts:
            return {
                'threat_type': 'BRUTE_FORCE',
                'severity': 'HIGH',
                'ip': ip,
                'service': service,
                'username': username,
                'failed_count': total_attempts,
                'threshold_limit': self.max_failed_attempts
            }

        return None
