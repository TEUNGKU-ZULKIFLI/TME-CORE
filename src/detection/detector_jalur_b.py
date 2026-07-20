# =================================================================
# FILE: src/detection/detector_jalur_b.py
# FUNGSI: Deteksi Anomali Jalur B - Brute Force Success Prevention
# =================================================================
import datetime
import time
from config import config
from src.firewall.mitigator_jalur_a import block_ip
from src.alert.notifier import send_telegram_alert
from src.db.state_manager import save_state
from src.monitoring.evaluator_jalur_b import record_performance_to_csv

def check_active_session_anomalies(api, failed_attempts, session_blocked_ips):

    try:
        # 1. Ambil semua pengguna yang sedang login aktif di MikroTik
        active_users = api.get_resource('/user/active').get()

        for user in active_users:
            session_id = user.get('.id')
            username = user.get('name')
            ip_address = user.get('address')
            via_service = user.get('via') # ssh, ftp, winbox, dll.

            if not ip_address:
                continue

            # Bersihkan IP jika ada port di belakangnya (contoh: 192.168.20.3:54321)
            ip_clean = ip_address.split(':')[0] if ':' in ip_address else ip_address

            # Abaikan jika IP berada di Whitelist
            if ip_clean in config.WHITELIST_IPS:
                continue

            # Abaikan jika IP sudah terblokir sebelumnya di sesi ini
            if ip_clean in session_blocked_ips:
                continue

            # 2. DETEKSI ANOMALI:
            if ip_clean in failed_attempts and failed_attempts[ip_clean] > 0:
                print(f"\033[91m[🚨 ANOMALI DETECTED]: IP {ip_clean} berhasil masuk sebagai '{username}' via {via_service}")
                print(f"                       setelah mengalami {failed_attempts[ip_clean]} kegagalan!\033[0m")
                print(f"[*] DEFENSIVE ACTION: Memblokir IP {ip_clean} di Firewall Address List...")
                sukses_blokir = block_ip(api, ip_clean)

                if sukses_blokir:
                    session_blocked_ips.add(ip_clean)
                    failed_count_temp = failed_attempts[ip_clean] # Simpan histori untuk alert telegram
                    del failed_attempts[ip_clean]
                    save_state(failed_attempts, session_blocked_ips) # Sinkronisasi database JSON
                else:
                    failed_count_temp = failed_attempts.get(ip_clean, 1)

                active_resource = api.get_resource('/user/active')
                session_kicked = False

                try:
                    # Skenario 1: Coba request-logout (Standar RouterOS v6.x & v7.x < 7.20)
                    active_resource.call('request-logout', {'numbers': session_id})
                    print(f"[+] MITIGASI JALUR B: Sesi aktif {ip_clean} diputus paksa (via request-logout API).")
                    session_kicked = True
                except Exception as e_logout:
                    err_msg = str(e_logout).lower()

                    # Jika Skenario 1 ditolak API karena limitasi RouterOS v6.x / v7.x
                    if "no such command" in err_msg or "not found" in err_msg or "unknown" in err_msg:
                        try:
                            # Skenario 2: Coba remove (Standar RouterOS v7.20+ atau Hotspot Active Session)
                            active_resource.remove(id=session_id)
                            print(f"[+] MITIGASI JALUR B: Sesi aktif {ip_clean} diputus paksa (via remove API).")
                            session_kicked = True
                        except Exception as e_remove:
                            # Skenario 3: ULTIMATE FALLBACK - Dynamic Scripting (Wajib untuk RouterOS v6.x Physical)
                            print(f"[*] INFO: Mencoba Skenario 3 (Dynamic Scripting Injection) untuk RouterOS v6.x...")
                            script_resource = api.get_resource('/system/script')
                            script_name = f"tme_kick_{int(time.time())}"
                            script_source = (
                                f':foreach i in=[/user/active/find] do={{'
                                f':local addr [/user/active/get $i address]; '
                                f':if ($addr ~ "{ip_clean}") do={{/user/active/request-logout numbers=$i}}'
                                f'}}'
                            )

                            try:
                                # A. Tambahkan script bypass sementara ke router
                                script_resource.add(
                                    name=script_name,
                                    source=script_source,
                                    policy="read,write,policy,test"
                                )

                                # B. Jalankan script dalam try-finally block agar pembersihan script dijamin berjalan
                                try:
                                    script_resource.call('run', {'number': script_name})
                                    print(f"[+] MITIGASI JALUR B: Sesi aktif {ip_clean} diputus paksa (via Local Script Injection).")
                                    session_kicked = True
                                finally:
                                    # C. ULTIMATE CLEANUP: Menghapus script sementara dari MikroTik
                                    script_to_remove = script_resource.get(name=script_name)
                                    if script_to_remove:
                                        script_resource.remove(id=script_to_remove[0]['id'])
                                        print("[*] JALUR B: Pembersihan script sementara berhasil dilakukan.")

                            except Exception as e_script:
                                print(f"[-] ERROR UTAMA MITIGASI JALUR B (Skenario 3 Gagal): {e_script}")
                    else:
                        print(f"[-] ERROR REQUEST-LOGOUT JALUR B: {e_logout}")

                # D. Deteksi tipe port layanan secara dinamis untuk laporan
                service_detected = "Unknown Service"
                if via_service == "ssh":
                    service_detected = "SSH (Port 22)"
                elif via_service == "ftp":
                    service_detected = "FTP (Port 21)"
                else:
                    service_detected = f"{via_service.upper()}"

                # E. Ekstrak beban Router & Tulis ke CSV (Kinerja)
                last_cpu, last_ram = 100, 8.0
                if sukses_blokir:
                    status_metrics = f"BYPASS BLOCKED JALUR B ({service_detected})" if session_kicked else "BYPASS BLOCKED (KICK FAILED)"
                    cpu, ram = record_performance_to_csv(api, ip_clean, status_metrics)
                    if cpu is not None:
                        last_cpu = cpu
                        last_ram = ram

                # F. Kirim Notifikasi Telegram Khusus Anomali
                status_mitigasi = "SESSION KICK & BLACKLIST DROP" if session_kicked else "BLACKLIST DROP ONLY (Kick Failed)"

                pesan_alert = (
                    f"🚨 <b>TME-CORE ANOMALY ALERT</b>\n"
                    f"───────────────────────────\n\n"
                    f"📌 <b>IP Penyerang</b> : <code>{ip_clean}</code>\n"
                    f"🌐 <b>Layanan/Port</b>  : <code>{service_detected}</code>\n"
                    f"🔑 <b>Username</b>     : <code>{username}</code>\n"
                    f"🛡️ <b>Status</b>       : BERHASIL LOGIN BYPASS (Anomali)\n"
                    f"⚡ <b>Aksi Mitigasi</b>: <code>{status_mitigasi}</code>\n"
                    f"📈 <b>Riwayat Gagal</b> : {failed_count_temp} kali\n\n"
                    f"📊 <b>METRIK SUMBER DAYA ROUTER:</b>\n"
                    f"  ├─ Beban CPU : {last_cpu}% (CRITICAL)\n"
                    f"  └─ Sisa RAM  : {last_ram:.2f} MB / 32.00 MB\n\n"
                    f"───────────────────────────\n"
                    f"📅 <i>Dilaporkan secara real-time oleh Jalur B Engine</i>"
                )

                # Gunakan parameter khusus custom_message
                send_telegram_alert(ip_clean, last_cpu, last_ram, custom_message=pesan_alert)
                return True

    except Exception as e:
        print(f"[-] ERROR JALUR B DETECTOR: {e}")

    return False
