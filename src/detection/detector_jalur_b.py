# =================================================================
# FILE: src/detection/detector_jalur_b.py
# FUNGSI: Deteksi Anomali Jalur B - Brute Force Success Prevention (OOP)
# =================================================================
import time
from typing import Dict, Any, List, Set, Optional
from config.config import WHITELIST_IPS
from src.firewall.mitigator_jalur_a import MitigatorJalurA
from src.db.state_manager import save_state
from src.monitoring.evaluator_jalur_b import record_performance_to_csv

class DetectorJalurB:
    def __init__(self, whitelist_ips: Optional[List[str]] = None):
        self.whitelist_ips = set(whitelist_ips) if whitelist_ips else set(WHITELIST_IPS)
        self.mitigator = MitigatorJalurA()

    def check_active_session_anomalies(self, api, failed_attempts: Dict[str, Any], 
                                      session_blocked_ips: Set[str], 
                                      persistent_failed_counts: Dict[str, dict] = None, 
                                      notifier=None) -> bool:
        """
        Memeriksa sesi user aktif di MikroTik (/user/active). 
        Membuat pemicu blokir & kick jika IP asing memiliki rekam jejak percobaan gagal.
        """
        if not api:
            return False

        if persistent_failed_counts is None:
            persistent_failed_counts = {}

        try:
            active_users = api.get_resource('/user/active').get()

            for user in active_users:
                session_id = user.get('.id')
                username = user.get('name')
                ip_address = user.get('address')
                via_service = user.get('via')

                if not ip_address:
                    continue

                # Bersihkan format IP jika menyertakan port
                ip_clean = ip_address.split(':')[0] if ':' in ip_address else ip_address

                # 1. Abaikan Whitelist & IP yang sudah terblokir
                if ip_clean in self.whitelist_ips or ip_clean in session_blocked_ips:
                    continue

                # 2. DETEKSI ANOMALI: Hitung gabungan histori kegagalan
                hist = failed_attempts.get(ip_clean, [])
                recent_fails = len(hist) if isinstance(hist, list) else 0
                
                p_entry = persistent_failed_counts.get(ip_clean, {})
                p_count = int(p_entry.get('count', 0)) if isinstance(p_entry, dict) else 0

                total_failed_history = recent_fails + p_count

                # Jika IP ini pernah gagal login tapi sekarang statusnya LOGIN AKTIF -> ANOMALI!
                if total_failed_history > 0:
                    print(f"\n\033[91m[🚨 ANOMALI JALUR B DETECTED]: IP {ip_clean} berhasil masuk sebagai '{username}' via {via_service}")
                    print(f"                               setelah mengalami {total_failed_history}x kegagalan!\033[0m")
                    print(f"[*] DEFENSIVE ACTION: Memblokir IP {ip_clean} di Firewall Address List...")

                    sukses_blokir = self.mitigator.block_ip_address_list(api, ip_clean, comment=f"TME-CORE ANOMALY {via_service}")

                    if sukses_blokir:
                        session_blocked_ips.add(ip_clean)
                        if ip_clean in failed_attempts:
                            del failed_attempts[ip_clean]
                        if ip_clean in persistent_failed_counts:
                            persistent_failed_counts[ip_clean] = {'count': 0, 'last': 0}
                        save_state(failed_attempts, session_blocked_ips, persistent_failed_counts)

                    # 3. KICK ACTIVE SESSION (3-Tier Fallback Mechanism)
                    active_resource = api.get_resource('/user/active')
                    session_kicked = False

                    # Skenario 1: API request-logout
                    try:
                        active_resource.call('request-logout', {'numbers': session_id})
                        print(f"[✓] MITIGASI JALUR B: Sesi aktif {ip_clean} diputus paksa (via request-logout).")
                        session_kicked = True
                    except Exception as e_logout:
                        err_msg = str(e_logout).lower()
                        if any(x in err_msg for x in ("no such command", "not found", "unknown")):
                            # Skenario 2: API remove
                            try:
                                active_resource.remove(id=session_id)
                                print(f"[✓] MITIGASI JALUR B: Sesi aktif {ip_clean} diputus paksa (via remove).")
                                session_kicked = True
                            except Exception:
                                # Skenario 3: Local Dynamic Script Injection (RouterOS v6.x fallback)
                                print(f"[*] INFO: Mencoba Skenario 3 (Dynamic Scripting Injection)...")
                                try:
                                    script_resource = api.get_resource('/system/script')
                                    script_name = f"tme_kick_{int(time.time())}"
                                    script_source = (
                                        f':foreach i in=[/user/active/find] do={{'
                                        f':local addr [/user/active/get $i address]; '
                                        f':if ($addr ~ "{ip_clean}") do={{/user/active/request-logout numbers=$i}}'
                                        f'}}'
                                    )
                                    script_resource.add(name=script_name, source=script_source, policy="read,write,policy,test")
                                    try:
                                        script_resource.call('run', {'number': script_name})
                                        print(f"[✓] MITIGASI JALUR B: Sesi aktif {ip_clean} diputus paksa (via Script Injection).")
                                        session_kicked = True
                                    finally:
                                        script_to_remove = script_resource.get(name=script_name)
                                        if script_to_remove:
                                            script_resource.remove(id=script_to_remove[0]['id'])
                                except Exception as e_script:
                                    print(f"[-] ERROR MITIGASI SKE3 JALUR B: {e_script}")
                        else:
                            print(f"[-] ERROR REQUEST-LOGOUT JALUR B: {e_logout}")

                    # 4. Catat evaluasi beban router ke CSV
                    service_detected = str(via_service).upper()
                    last_cpu, last_ram = None, None
                    if sukses_blokir:
                        status_metrics = f"BYPASS_BLOCKED {'(Session Kicked)' if session_kicked else '(Kick Failed)'}"
                        try:
                            last_cpu, last_ram = record_performance_to_csv(api, ip_clean, status_metrics)
                        except Exception:
                            pass

                    # 5. Kirim Notifikasi Telegram
                    if notifier:
                        try:
                            threat_data = {
                                'threat_type': 'BYPASS_BLOCKED',
                                'severity': 'CRITICAL',
                                'ip': ip_clean,
                                'service': service_detected,
                                'username': username
                            }
                            notifier.send_alert(threat_data, cpu=last_cpu, ram_mb=last_ram, failed_count=total_failed_history)
                        except Exception as e_nt:
                            print(f"[!] Gagal mengirim notifikasi anomali: {e_nt}")

                    return True

        except Exception as e:
            print(f"[-] ERROR JALUR B DETECTOR: {e}")

        return False


# --- Blok Testing Mandiri ---
if __name__ == "__main__":
    print("=== TESTING MODUL DETECTOR JALUR B ===")
    
    # Mocking RouterOS Active User API
    class MockActiveResource:
        def get(self):
            return [{'.id': '*B1', 'name': 'admin', 'address': '192.168.20.77', 'via': 'ssh'}]
        def call(self, cmd, params):
            print(f"    [Mock API] Perintah '{cmd}' dipanggil dengan parameter: {params}")

    class MockAPI:
        def get_resource(self, path): return MockActiveResource()

    detector_b = DetectorJalurB(whitelist_ips=['192.168.10.1'])
    
    # Simulasi data state
    dummy_failed = {'192.168.20.77': [time.time() - 10]} # IP ini pernah gagal login
    dummy_blocked = set()
    dummy_pfc = {}

    print("[*] Menjalankan pemindaian anomali Jalur B...")
    detected = detector_b.check_active_session_anomalies(MockAPI(), dummy_failed, dummy_blocked, dummy_pfc)
    print(f"[*] Status Anomali Terdeteksi: {detected}")
