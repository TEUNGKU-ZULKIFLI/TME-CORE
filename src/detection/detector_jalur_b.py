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

                ip_clean = ip_address.split(':')[0] if ':' in ip_address else ip_address

                if ip_clean in self.whitelist_ips or ip_clean in session_blocked_ips:
                    continue

                hist = failed_attempts.get(ip_clean, [])
                recent_fails = len(hist) if isinstance(hist, list) else 0

                p_entry = persistent_failed_counts.get(ip_clean, {})
                p_count = int(p_entry.get('count', 0)) if isinstance(p_entry, dict) else 0

                total_failed_history = max(recent_fails, p_count)

                print(f"\n[🚨 ANOMALI JALUR B DETECTED]: AKSES ILEGAL! IP {ip_clean} (Non-Whitelist)")
                print(f"                               berhasil masuk sebagai '{username}' via {via_service}")
                print(f"                               (Histori kegagalan sebelumnya: {total_failed_history}x)")
                print(f"[*] DEFENSIVE ACTION: Memblokir IP {ip_clean} di Firewall Address List...")

                sukses_blokir = self.mitigator.block_ip_address_list(api, ip_clean, comment=f"TME-CORE ANOMALY {via_service}")

                if sukses_blokir:
                    session_blocked_ips.add(ip_clean)
                    if ip_clean in failed_attempts:
                        del failed_attempts[ip_clean]
                    if ip_clean in persistent_failed_counts:
                        persistent_failed_counts[ip_clean] = {'count': 0, 'last': 0}
                    save_state(failed_attempts, session_blocked_ips, persistent_failed_counts)

                active_resource = api.get_resource('/user/active')
                session_kicked = False

                try:
                    active_resource.call('request-logout', {'numbers': session_id})
                    print(f"[✓] MITIGASI JALUR B: Sesi aktif {ip_clean} diputus paksa (via request-logout).")
                    session_kicked = True
                except Exception as e_logout:
                    err_msg = str(e_logout).lower()
                    if any(x in err_msg for x in ("no such command", "not found", "unknown")):
                        try:
                            active_resource.remove(id=session_id)
                            print(f"[✓] MITIGASI JALUR B: Sesi aktif {ip_clean} diputus paksa (via remove).")
                            session_kicked = True
                        except Exception:
                            print(f"[*] INFO: Mencoba Skenario 3 (Firewall Connection Teardown)...")
                            try:
                                killed = self.mitigator.kill_active_session(api, ip_clean)
                                if killed > 0:
                                    print(f"[✓] MITIGASI JALUR B: Sesi aktif {ip_clean} diputus paksa (via Firewall Connection Kill).")
                                    session_kicked = True
                                else:
                                    print(f"[✓] MITIGASI JALUR B: IP {ip_clean} berhasil di-drop oleh Firewall Address List.")
                                    session_kicked = True
                            except Exception as e_kill:
                                print(f"[-] ERROR MITIGASI SKE3 JALUR B: {e_kill}")
                    else:
                        print(f"[-] ERROR REQUEST-LOGOUT JALUR B: {e_logout}")

                service_detected = str(via_service).upper()
                last_cpu, last_ram = None, None
                if sukses_blokir:
                    status_metrics = f"UNAUTHORIZED_SUCCESS {'(Session Kicked)' if session_kicked else '(Kick Failed)'}"
                    try:
                        last_cpu, last_ram = record_performance_to_csv(api, ip_clean, status_metrics)
                    except Exception:
                        pass

                if notifier:
                    try:
                        threat_data = {
                            'threat_type': 'UNAUTHORIZED_SUCCESS',
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
