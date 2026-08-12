# ==========================================
# FILE: src/detection/detector_jalur_a.py
# FUNGSI: Jalur A - Mendeteksi log Brute Force (menggunakan failed_attempts eksternal)
# ==========================================
import time
from typing import Dict, Any, Optional, List

class DetectorJalurA:
    def __init__(self, whitelist_ips: List[str], max_failed_attempts: int = 5, time_window_seconds: int = 60):
        self.whitelist_ips = set(whitelist_ips)
        self.max_failed_attempts = max_failed_attempts
        self.time_window_seconds = time_window_seconds

    def _prune(self, lst: List[float]) -> List[float]:
        now = time.time()
        return [t for t in lst if (now - t) <= self.time_window_seconds]

    def analyze_log(self, parsed_log: Dict[str, Any], failed_attempts: Dict[str, List[float]], persistent_failed_counts: Dict[str, dict] = None) -> Optional[Dict[str, Any]]:
        if not parsed_log:
            return None

        ip = parsed_log.get('ip')
        status = parsed_log.get('status')
        service = parsed_log.get('service')
        username = parsed_log.get('username')

        if not ip:
            return None

        # Abaikan whitelist
        if ip in self.whitelist_ips:
            return None

        # Ensure persistent_failed_counts shape
        if persistent_failed_counts is None:
            persistent_failed_counts = {}

        # SUCCESS case: jika ada histori gagal recent => UNAUTHORIZED_SUCCESS
        if status == 'SUCCESS':
            hist = failed_attempts.get(ip, [])
            if not isinstance(hist, list):
                hist = []
            hist = self._prune(hist)
            failed_attempts[ip] = hist

            persistent_entry = persistent_failed_counts.get(ip, {'count': 0, 'last': 0})
            persistent_count = int(persistent_entry.get('count', 0)) if isinstance(persistent_entry.get('count', 0), int) else 0

            total_recent = len(hist) + persistent_count
            if total_recent > 0:
                # leave cleanup to caller after mitigation, but return threat
                return {
                    'threat_type': 'UNAUTHORIZED_SUCCESS',
                    'severity': 'CRITICAL',
                    'ip': ip,
                    'service': service,
                    'username': username,
                    'message': f"🚨 CRITICAL ALERT: IP {ip} berhasil login via {service} setelah {total_recent} kegagalan!",
                    'failed_count': total_recent
                }
            return None

        # FAILED case: tambahkan timestamp dan periksa ambang
        if status == 'FAILED':
            now = time.time()
            lst = failed_attempts.get(ip, [])
            if not isinstance(lst, list):
                lst = []
            lst.append(now)
            lst = self._prune(lst)
            failed_attempts[ip] = lst

            persistent_entry = persistent_failed_counts.get(ip, {'count': 0, 'last': 0})
            persistent_count = int(persistent_entry.get('count', 0)) if isinstance(persistent_entry.get('count', 0), int) else 0

            total_recent = len(lst) + persistent_count

            if total_recent >= self.max_failed_attempts:
                # reset history agar tidak memicu berulang
                failed_attempts[ip] = []
                # also reset persistent counter (caller should persist save_state after mitigation)
                persistent_failed_counts[ip] = {'count': 0, 'last': 0}
                return {
                    'threat_type': 'BRUTE_FORCE',
                    'severity': 'HIGH',
                    'ip': ip,
                    'service': service,
                    'username': username,
                    'failed_count': total_recent,
                    'threshold_limit': self.max_failed_attempts,
                    'message': f"⚠️ BRUTE_FORCE: IP {ip} mencapai {total_recent}/{self.max_failed_attempts} percobaan via {service}!"
                }

        return None
