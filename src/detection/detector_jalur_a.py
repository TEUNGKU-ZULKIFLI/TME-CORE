# ==========================================
# FILE: src/detection/detector_jalur_a.py
# FUNGSI: Jalur A - Detektor Akses Ilegal (1x Tembus) & Brute Force
# ==========================================
import time
from typing import Dict, Any, Optional, List

class DetectorJalurA:
    def __init__(self, whitelist_ips: List[str], max_failed_attempts: int = 5, time_window_seconds: int = 60):
        self.whitelist_ips = set(whitelist_ips)
        self.max_failed_attempts = max_failed_attempts
        self.time_window_seconds = time_window_seconds

    def _prune(self, lst: List[float]) -> List[float]:
        """Menghapus timestamp percobaan yang sudah di luar jendela waktu (time_window)."""
        now = time.time()
        return [t for t in lst if (now - t) <= self.time_window_seconds]

    def analyze_log(self, parsed_log: Dict[str, Any], failed_attempts: Dict[str, List[float]] = None, persistent_failed_counts: Dict[str, dict] = None) -> Optional[Dict[str, Any]]:
        if not parsed_log:
            return None

        ip = parsed_log.get('ip')
        status = parsed_log.get('status')
        service = parsed_log.get('service')
        username = parsed_log.get('username')

        if not ip:
            return None

        # 1. Abaikan IP Whitelist (IP resmi pengelola router)
        if ip in self.whitelist_ips:
            return None

        if failed_attempts is None:
            failed_attempts = {}
        if persistent_failed_counts is None:
            persistent_failed_counts = {}

        # 2. KASUS LOGIN SUKSES dari IP Non-Whitelist -> AKSES ILEGAL (1x TEMBUS / UNAUTHORIZED SUCCESS)
        if status == 'SUCCESS':
            hist = failed_attempts.get(ip, [])
            if not isinstance(hist, list):
                hist = []
            hist = self._prune(hist)
            failed_attempts[ip] = hist

            persistent_entry = persistent_failed_counts.get(ip, {'count': 0, 'last': 0})
            persistent_count = int(persistent_entry.get('count', 0)) if isinstance(persistent_entry.get('count', 0), int) else 0

            total_recent = len(hist) + persistent_count
            
            # Formulasi pesan deteksi yang informatif
            if total_recent > 0:
                msg = f"🚨 CRITICAL ALERT: IP Asing {ip} berhasil login via {service} sebagai user '{username}' setelah {total_recent}x kegagalan!"
            else:
                msg = f"🚨 CRITICAL ALERT: Akses Ilegal Terdeteksi! IP Asing {ip} berhasil login via {service} sebagai user '{username}'!"

            return {
                'threat_type': 'UNAUTHORIZED_SUCCESS',
                'severity': 'CRITICAL',
                'ip': ip,
                'service': service,
                'username': username,
                'message': msg,
                'failed_count': total_recent
            }

        # 3. KASUS LOGIN GAGAL dari IP Non-Whitelist -> PERCOBAAN BRUTE FORCE
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

            # Jika jumlah kegagalan mencapai batas threshold -> Pemicu Brute Force Threat
            if total_recent >= self.max_failed_attempts:
                # Reset histori agar tidak triger berulang-ulang
                failed_attempts[ip] = []
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


# --- Blok Testing Mandiri ---
if __name__ == "__main__":
    print("=== TESTING MODUL DETECTOR JALUR A ===")
    whitelist = ['192.168.10.2', '127.0.0.1']
    detector = DetectorJalurA(whitelist_ips=whitelist, max_failed_attempts=3)
    
    failed_attempts_db = {}
    persistent_counts_db = {}

    # Tes 1: Whitelist login (Harus Diabaikan)
    log_wl = {'ip': '192.168.10.2', 'status': 'SUCCESS', 'service': 'api', 'username': 'admin'}
    print("\n[*] Testing Whitelist Login:")
    print(f"    Result: {detector.analyze_log(log_wl, failed_attempts_db, persistent_counts_db)}")

    # Tes 2: IP Asing Login Langsung Sukses (1x Tembus)
    log_tembus = {'ip': '192.168.20.50', 'status': 'SUCCESS', 'service': 'ssh', 'username': 'admin'}
    print("\n[*] Testing 1x Tembus langsung (IP Asing):")
    threat1 = detector.analyze_log(log_tembus, failed_attempts_db, persistent_counts_db)
    if threat1:
        print(f"    [✓] DETECTED: {threat1['threat_type']} -> {threat1['message']}")

    # Tes 3: Simulasi Brute Force 3x percobaan (Threshold = 3)
    log_fail = {'ip': '192.168.20.99', 'status': 'FAILED', 'service': 'ssh', 'username': 'admin'}
    print("\n[*] Testing Brute Force Simulation (IP: 192.168.20.99):")
    for i in range(1, 4):
        threat = detector.analyze_log(log_fail, failed_attempts_db, persistent_counts_db)
        if threat:
            print(f"    [✓] Attempt #{i}: DETECTED! {threat['threat_type']} -> {threat['message']}")
        else:
            print(f"    [-] Attempt #{i}: Recorded failed attempt.")
