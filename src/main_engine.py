# ==========================================
# FILE: src/main_engine.py
# FUNGSI: Orkestrator Utama TME-CORE
# ==========================================
import time
import os
import sys
import datetime

from config.config import (
    WHITELIST_IPS, MAX_FAILED_ATTEMPTS, ADDRESS_LIST_NAME, BLOCK_TIMEOUT,
    TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, SYSTEM_LOG_PATH, DATA_DIR
)
from src.api.connection import connect_to_mikrotik, disconnect_from_mikrotik
from src.parser.log_parser import parse_single_log
from src.detection.detector_jalur_a import DetectorJalurA
from src.firewall.mitigator_jalur_a import MitigatorJalurA
from src.alert.notifier import TelegramNotifier
from src.db.state_manager import load_state, save_state
from src.monitoring.evaluator_jalur_b import record_performance_to_csv
from src.detection.detector_jalur_b import DetectorJalurB # PERBAIKAN: Import Class DetectorJalurB
from src.cli.console import print_banner, run_doctor
import config.config as cfg

CHECKPOINT_INTERVAL = 30  # detik: interval menyimpan state ke disk

def write_system_log(message: str):
    try:
        # PERBAIKAN: Penulisan datetime yang benar
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    try:
        log_dir = os.path.dirname(SYSTEM_LOG_PATH)
        os.makedirs(log_dir, exist_ok=True)
        with open(SYSTEM_LOG_PATH, "a", encoding='utf-8') as f:
            f.write(f"[{timestamp}] {message}\n")
    except Exception as e:
        print(f"[✗] Gagal menulis system log: {e}")


def run_tme_engine():
    # Tampilkan banner dan pre-flight
    print_banner()
    run_doctor(cfg.ENV_PATH, cfg.DATA_DIR, cfg)

    # Load persistent state dari JSON
    # Pastikan file state_manager.py Anda mengembalikan 5 nilai ini.
    failed_attempts, session_blocked_ips, persistent_failed_counts, total_attacks_detected, total_attacks_blocked = load_state()

    # Inisialisasi Modul-modul Utama
    detector_a = DetectorJalurA(
        whitelist_ips=WHITELIST_IPS,
        max_failed_attempts=MAX_FAILED_ATTEMPTS,
        time_window_seconds=60
    )
    # PERBAIKAN: Inisialisasi DetectorJalurB
    detector_b = DetectorJalurB(whitelist_ips=WHITELIST_IPS)
    
    mitigator = MitigatorJalurA(
        address_list_name=ADDRESS_LIST_NAME,
        block_timeout=BLOCK_TIMEOUT
    )
    notifier = TelegramNotifier(
        token=TELEGRAM_TOKEN,
        chat_id=TELEGRAM_CHAT_ID
    )

    processed_log_ids = set()
    first_run = True
    last_checkpoint = time.time()

    print(f"[*] Konfigurasi Engine:")
    print(f"    ├─ Whitelist IP : {WHITELIST_IPS}")
    print(f"    ├─ Address List : {ADDRESS_LIST_NAME}")
    print(f"    ├─ Block Timeout: {BLOCK_TIMEOUT}")
    print(f"    └─ Threshold    : {MAX_FAILED_ATTEMPTS} attempts / 60 detik\n")

    write_system_log("TME-CORE Engine dimulai (atau restart).")

    try:
        while True:
            api, pool = connect_to_mikrotik()
            if not api:
                print("[✗] Gagal terhubung ke MikroTik. Mencoba lagi dalam 5 detik...")
                time.sleep(5)
                continue

            try:
                raw_logs = api.get_resource('/log').get()

                # Tandai semua log lama pada first run agar tidak membombardir notifikasi saat startup
                if first_run:
                    for log in raw_logs:
                        log_id = log.get('id')
                        if log_id:
                            processed_log_ids.add(log_id)
                    print(f"[✓] Monitoring Aktif. Mengabaikan {len(processed_log_ids)} log lama. Menunggu kejadian baru...")
                    first_run = False
                    disconnect_from_mikrotik(pool)
                    time.sleep(2)
                    continue

                # ==========================================
                # JALUR A: DETEKSI LOG & BRUTE FORCE
                # ==========================================
                for log in raw_logs:
                    log_id = log.get('id')
                    if not log_id or log_id in processed_log_ids:
                        continue

                    processed_log_ids.add(log_id)
                    parsed_log = parse_single_log(log)
                    if not parsed_log:
                        continue

                    raw_message = parsed_log.get('raw_message', '')
                    print(f"\n[+] LOG BARU TERDETEKSI: {raw_message}")

                    ip = parsed_log.get('ip')
                    status = parsed_log.get('status')

                    # PRE-CAPTURE histori sebelum di-reset oleh detector
                    pre_recent = len(failed_attempts.get(ip, [])) if ip else 0
                    pre_persistent = persistent_failed_counts.get(ip, {}).get('count', 0) if ip else 0

                    # UPDATE retensi ancaman (persistent_failed_counts)
                    now_ts = time.time()
                    if status == 'FAILED' and ip and ip not in WHITELIST_IPS:
                        pentry = persistent_failed_counts.get(ip, {'count': 0, 'last': 0})
                        last_ts = pentry.get('last', 0)
                        retention = cfg.STATE_RETENTION_SECONDS
                        if (now_ts - last_ts) <= retention:
                            pentry['count'] = pentry.get('count', 0) + 1
                        else:
                            pentry['count'] = 1
                        pentry['last'] = now_ts
                        persistent_failed_counts[ip] = pentry

                    # Analisa Jalur A
                    threat = detector_a.analyze_log(parsed_log, failed_attempts, persistent_failed_counts)

                    # Jika gagal login, simpan jejak
                    if status == 'FAILED' and ip and ip not in WHITELIST_IPS:
                        post_persistent = persistent_failed_counts.get(ip, {}).get('count', 0)
                        post_recent = len(failed_attempts.get(ip, [])) if ip else 0
                        post_total = post_recent + post_persistent
                        threshold_info = f" [Threshold: {cfg.MAX_FAILED_ATTEMPTS}]" if post_total >= (cfg.MAX_FAILED_ATTEMPTS - 2) else ""
                        write_system_log(f"Gagal login dari {ip} (recent={pre_recent}→{post_recent} | persist={pre_persistent}→{post_persistent} | total={post_total}{threshold_info})")
                        save_state(failed_attempts, session_blocked_ips, persistent_failed_counts, total_attacks_detected, total_attacks_blocked)
                    
                    if threat:
                        # Terdeteksi ancaman nyata
                        total_attacks_detected += 1
                        threat_type = threat.get('threat_type', 'UNKNOWN')
                        failed_count = threat.get('failed_count', 0)
                        threshold_limit = threat.get('threshold_limit', '?')
                        write_system_log(f"[⚠️] DETECTED: {threat_type} from {threat.get('ip')} [Attempts: {failed_count}/{threshold_limit}]")

                        # Ekstraksi Beban CPU & RAM untuk Notifikasi
                        cpu_load, ram_free = None, None
                        try:
                            resources = api.get_resource('/system/resource').get()
                            if resources:
                                res_data = resources[0]
                                cpu_load = int(res_data.get('cpu-load', 0))
                                ram_free = int(res_data.get('free-memory', 0)) / (1024 * 1024)
                        except Exception:
                            pass

                        # Eksekusi mitigasi
                        try:
                            mitigasi_ok = mitigator.execute_mitigation(api, threat)
                        except Exception as e:
                            mitigasi_ok = False
                            print(f"[✗] Error saat mitigasi: {e}")

                        hist_count = None
                        if mitigasi_ok:
                            total_attacks_blocked += 1
                            t_ip = threat.get('ip')
                            hist_count = len(failed_attempts.get(t_ip, [])) if isinstance(failed_attempts.get(t_ip), list) else 0
                            
                            # Hapus riwayat IP setelah diblokir
                            if t_ip and t_ip in failed_attempts:
                                del failed_attempts[t_ip]
                            if t_ip and t_ip in persistent_failed_counts:
                                persistent_failed_counts[t_ip] = {'count': 0, 'last': 0}
                            save_state(failed_attempts, session_blocked_ips, persistent_failed_counts, total_attacks_detected, total_attacks_blocked)

                            # Rekam metrik
                            try:
                                cpu, ram = record_performance_to_csv(api, threat.get('ip'), f"MITIGATED: {threat.get('threat_type')}")
                                if cpu is not None: cpu_load = cpu
                                if ram is not None: ram_free = ram
                            except Exception:
                                pass

                        # Kirim Alert ke Telegram
                        try:
                            notifier.send_alert(threat, cpu=cpu_load, ram_mb=ram_free, failed_count=hist_count)
                        except Exception as e:
                            print(f"[✗] Gagal mengirim notifikasi: {e}")

                # ==========================================
                # JALUR B: DETEKSI ANOMALI SESI AKTIF
                # ==========================================
                try:
                    # PERBAIKAN: Pemanggilan metode dari instance detector_b
                    anomaly_found = detector_b.check_active_session_anomalies(
                        api, failed_attempts, session_blocked_ips, persistent_failed_counts, notifier
                    )
                    if anomaly_found:
                        save_state(failed_attempts, session_blocked_ips, persistent_failed_counts, total_attacks_detected, total_attacks_blocked)
                except Exception as e:
                    print(f"[✗] Error pada pemeriksaan Jalur B: {e}")

            except Exception as e:
                print(f"[✗] Error saat membaca/memproses log: {e}")
                write_system_log(f"ENGINE ERROR: {e}")

            finally:
                disconnect_from_mikrotik(pool)

            # Auto-save State setiap CHECKPOINT_INTERVAL
            now = time.time()
            if now - last_checkpoint >= CHECKPOINT_INTERVAL:
                save_state(failed_attempts, session_blocked_ips, persistent_failed_counts, total_attacks_detected, total_attacks_blocked)
                last_checkpoint = now

            time.sleep(2) # Interval polling utama

    except KeyboardInterrupt:
        print("\n\n[!] TME-CORE Engine dihentikan secara aman oleh pengguna.")
        write_system_log("Sistem dihentikan manual oleh Administrator (Ctrl+C).")
        save_state(failed_attempts, session_blocked_ips, persistent_failed_counts, total_attacks_detected, total_attacks_blocked)
        sys.exit(0)

if __name__ == "__main__":
    run_tme_engine()
