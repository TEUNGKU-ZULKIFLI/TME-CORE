# =================================================================
# FILE: src/detection/detector_jalur_b.py
# FUNGSI: Deteksi Anomali Jalur B - Brute Force Success Prevention
# =================================================================
import time
from config.config import WHITELIST_IPS
from src.firewall.mitigator_jalur_a import MitigatorJalurA
from src.db.state_manager import save_state
from src.monitoring.evaluator_jalur_b import record_performance_to_csv

_mitigator = MitigatorJalurA()


def check_active_session_anomalies(api, failed_attempts, session_blocked_ips, persistent_failed_counts=None, notifier=None):
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

            if ip_clean in WHITELIST_IPS:
                continue

            if ip_clean in session_blocked_ips:
                continue

            # DETEKSI ANOMALI: jika IP memiliki histori gagal login sebelumnya
            hist = failed_attempts.get(ip_clean, []) if failed_attempts is not None else []
            count = len(hist) if isinstance(hist, list) else (hist if isinstance(hist, int) else 0)
            if count > 0:
                print(f"\033[91m[🚨 ANOMALI DETECTED]: IP {ip_clean} berhasil masuk sebagai '{username}' via {via_service}")
                print(f"                       setelah mengalami {count} kegagalan!\033[0m")
                print(f"[*] DEFENSIVE ACTION: Memblokir IP {ip_clean} di Firewall Address List...")

                sukses_blokir = _mitigator.block_ip_address_list(api, ip_clean, comment=f"TME-CORE ANOMALY {via_service}")

                if sukses_blokir:
                    session_blocked_ips.add(ip_clean)
                    failed_count_temp = count
                    if ip_clean in failed_attempts:
                        del failed_attempts[ip_clean]
                    # Reset persistent_failed_counts if present
                    if persistent_failed_counts is not None and ip_clean in persistent_failed_counts:
                        persistent_failed_counts[ip_clean] = {'count': 0, 'last': 0}
                    save_state(failed_attempts, session_blocked_ips, persistent_failed_counts)
                else:
                    failed_count_temp = count

                active_resource = api.get_resource('/user/active')
                session_kicked = False

                try:
                    active_resource.call('request-logout', {'numbers': session_id})
                    print(f"[+] MITIGASI JALUR B: Sesi aktif {ip_clean} diputus paksa (via request-logout API).")
                    session_kicked = True
                except Exception as e_logout:
                    err_msg = str(e_logout).lower()

                    if any(x in err_msg for x in ("no such command", "not found", "unknown")):
                        try:
                            active_resource.remove(id=session_id)
                            print(f"[+] MITIGASI JALUR B: Sesi aktif {ip_clean} diputus paksa (via remove API).")
                            session_kicked = True
                        except Exception:
                            print(f"[*] INFO: Mencoba Skenario 3 (Dynamic Scripting Injection) untuk RouterOS v6.x...")
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
                                    print(f"[+] MITIGASI JALUR B: Sesi aktif {ip_clean} diputus paksa (via Local Script Injection).")
                                    session_kicked = True
                                finally:
                                    script_to_remove = script_resource.get(name=script_name)
                                    if script_to_remove:
                                        script_resource.remove(id=script_to_remove[0]['id'])
                                        print("[*] JALUR B: Pembersihan script sementara berhasil dilakukan.")

                            except Exception as e_script:
                                print(f"[-] ERROR UTAMA MITIGASI JALUR B (Skenario 3 Gagal): {e_script}")
                    else:
                        print(f"[-] ERROR REQUEST-LOGOUT JALUR B: {e_logout}")

                # Deteksi tipe port layanan
                service_detected = "SSH (Port 22)" if via_service == "ssh" else \
                                 "FTP (Port 21)" if via_service == "ftp" else \
                                 f"{str(via_service).upper()}"

                # Ambil CPU/RAM saat block
                last_cpu = None
                last_ram = None
                if sukses_blokir:
                    status_metrics = f"BYPASS_BLOCKED {'(Session Kicked)' if session_kicked else '(Kick Failed)'}"
                    try:
                        cpu, ram = record_performance_to_csv(api, ip_clean, status_metrics)
                        if cpu is not None:
                            last_cpu = cpu
                        if ram is not None:
                            last_ram = ram
                    except Exception:
                        pass

                # Kirim notifikasi via template terpadu
                if notifier:
                    try:
                        threat_data = {
                            'threat_type': 'BYPASS_BLOCKED',
                            'severity': 'CRITICAL',
                            'ip': ip_clean,
                            'service': service_detected,
                            'username': username
                        }
                        notifier.send_alert(threat_data, cpu=last_cpu, ram_mb=last_ram, failed_count=failed_count_temp)
                    except Exception as e_nt:
                        print(f"[!] Gagal mengirim notifikasi anomali: {e_nt}")

                return True

    except Exception as e:
        print(f"[-] ERROR JALUR B DETECTOR: {e}")

    return False
