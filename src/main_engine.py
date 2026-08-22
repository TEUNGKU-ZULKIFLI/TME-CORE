import time
import os
import sys
import datetime

import config.config as cfg
from config.config import (
    WHITELIST_IPS, MAX_FAILED_ATTEMPTS, ADDRESS_LIST_NAME, BLOCK_TIMEOUT,
    TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, SYSTEM_LOG_PATH, DATA_DIR
)
from src.api.connection import connect_to_mikrotik, disconnect_from_mikrotik
from src.parser.log_parser import parse_single_log
from src.detection.detector_jalur_a import DetectorJalurA
from src.detection.detector_jalur_b import DetectorJalurB
from src.firewall.mitigator_jalur_a import MitigatorJalurA
from src.alert.notifier import TelegramNotifier
from src.db.state_manager import load_state, save_state
from src.monitoring.evaluator_jalur_b import record_performance_to_csv
from src.cli.console import print_banner, run_doctor

CHECKPOINT_INTERVAL = 30

def write_system_log(message: str):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        os.makedirs(os.path.dirname(SYSTEM_LOG_PATH), exist_ok=True)
        with open(SYSTEM_LOG_PATH, "a", encoding='utf-8') as f:
            f.write(f"[{timestamp}] {message}\n")
    except Exception as e:
        print(f"[✗] Gagal menulis system log: {e}")

def run_tme_engine():
    print_banner()
    run_doctor(cfg.ENV_PATH, cfg.DATA_DIR, cfg)

    failed_attempts, session_blocked_ips, persistent_failed_counts, total_attacks_detected, total_attacks_blocked = load_state()

    detector_a = DetectorJalurA(
        whitelist_ips=WHITELIST_IPS,
        max_failed_attempts=MAX_FAILED_ATTEMPTS,
        time_window_seconds=60
    )
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

    print("[*] Konfigurasi Engine:")
    print(f"    ├─ Whitelist IP : {WHITELIST_IPS}")
    print(f"    ├─ Address List : {ADDRESS_LIST_NAME}")
    print(f"    ├─ Block Timeout: {BLOCK_TIMEOUT}")
    print(f"    └─ Threshold    : {MAX_FAILED_ATTEMPTS} attempts / 60 detik\n")

    write_system_log("TME-CORE Engine dimulai.")

    try:
        while True:
            # Menggunakan quiet=True agar terminal tidak diserang spam log koneksi setiap 2 detik
            api, pool = connect_to_mikrotik(quiet=True)
            if not api:
                print("[✗] Gagal terhubung ke MikroTik. Retrying in 5s...")
                time.sleep(5)
                continue

            try:
                raw_logs = api.get_resource('/log').get()

                if first_run:
                    processed_log_ids.update(log.get('id') for log in raw_logs if log.get('id'))
                    print(f"[✓] Monitoring Aktif. Mengabaikan {len(processed_log_ids)} log lama.")
                    first_run = False
                    disconnect_from_mikrotik(pool, quiet=True)
                    time.sleep(2)
                    continue

                for log in raw_logs:
                    log_id = log.get('id')
                    if not log_id or log_id in processed_log_ids:
                        continue

                    processed_log_ids.add(log_id)
                    parsed_log = parse_single_log(log)
                    if not parsed_log:
                        continue

                    print(f"\n[+] LOG BARU: {parsed_log.get('raw_message', '')}")
                    ip = parsed_log.get('ip')
                    status = parsed_log.get('status')
                    now_ts = time.time()

                    if status == 'FAILED' and ip and ip not in WHITELIST_IPS:
                        pentry = persistent_failed_counts.get(ip, {'count': 0, 'last': 0})
                        if (now_ts - pentry.get('last', 0)) <= cfg.STATE_RETENTION_SECONDS:
                            pentry['count'] += 1
                        else:
                            pentry['count'] = 1
                        pentry['last'] = now_ts
                        persistent_failed_counts[ip] = pentry

                    threat = detector_a.analyze_log(parsed_log, failed_attempts, persistent_failed_counts)

                    if status == 'FAILED' and ip and ip not in WHITELIST_IPS:
                        post_persistent = persistent_failed_counts.get(ip, {}).get('count', 0)
                        post_recent = len(failed_attempts.get(ip, []))
                        thresh_info = f" [Threshold: {cfg.MAX_FAILED_ATTEMPTS}]" if post_persistent >= (cfg.MAX_FAILED_ATTEMPTS - 1) else ""
                        write_system_log(f"Gagal login dari {ip} (recent_60s={post_recent} | total_retention={post_persistent}{thresh_info})")
                        save_state(failed_attempts, session_blocked_ips, persistent_failed_counts, total_attacks_detected, total_attacks_blocked)
                    
                    if threat:
                        total_attacks_detected += 1
                        t_ip = threat.get('ip')
                        write_system_log(f"[⚠️] DETECTED: {threat.get('threat_type')} from {t_ip} [Attempts: {threat.get('failed_count')}/{threat.get('threshold_limit')}]")

                        cpu_load, ram_free = None, None
                        try:
                            resources = api.get_resource('/system/resource').get()
                            if resources:
                                cpu_load = int(resources[0].get('cpu-load', 0))
                                ram_free = int(resources[0].get('free-memory', 0)) / (1024 * 1024)
                        except Exception:
                            pass

                        mitigasi_ok = False
                        try:
                            mitigasi_ok = mitigator.execute_mitigation(api, threat)
                        except Exception as e:
                            print(f"[✗] Error mitigasi: {e}")

                        hist_count = None
                        if mitigasi_ok:
                            total_attacks_blocked += 1
                            hist_count = len(failed_attempts.get(t_ip, []))
                            
                            if t_ip in failed_attempts:
                                del failed_attempts[t_ip]
                            if t_ip in persistent_failed_counts:
                                persistent_failed_counts[t_ip] = {'count': 0, 'last': 0}
                            save_state(failed_attempts, session_blocked_ips, persistent_failed_counts, total_attacks_detected, total_attacks_blocked)

                            try:
                                c, r = record_performance_to_csv(api, t_ip, f"MITIGATED: {threat.get('threat_type')}")
                                cpu_load = c if c is not None else cpu_load
                                ram_free = r if r is not None else ram_free
                            except Exception:
                                pass

                        try:
                            notifier.send_alert(threat, cpu=cpu_load, ram_mb=ram_free, failed_count=hist_count)
                        except Exception as e:
                            print(f"[✗] Gagal kirim Telegram: {e}")

                try:
                    if detector_b.check_active_session_anomalies(api, failed_attempts, session_blocked_ips, persistent_failed_counts, notifier):
                        save_state(failed_attempts, session_blocked_ips, persistent_failed_counts, total_attacks_detected, total_attacks_blocked)
                except Exception as e:
                    print(f"[✗] Error Jalur B: {e}")

            except Exception as e:
                print(f"[✗] Engine Loop Error: {e}")
                write_system_log(f"ENGINE ERROR: {e}")
            finally:
                # Menggunakan quiet=True untuk menghindari spam log putus koneksi
                disconnect_from_mikrotik(pool, quiet=True)

            now = time.time()
            if now - last_checkpoint >= CHECKPOINT_INTERVAL:
                save_state(failed_attempts, session_blocked_ips, persistent_failed_counts, total_attacks_detected, total_attacks_blocked)
                last_checkpoint = now

            time.sleep(2)

    except KeyboardInterrupt:
        print("\n\n[!] TME-CORE dihentikan secara aman.")
        write_system_log("Sistem dihentikan manual oleh Administrator (Ctrl+C).")
        save_state(failed_attempts, session_blocked_ips, persistent_failed_counts, total_attacks_detected, total_attacks_blocked)
        sys.exit(0)

if __name__ == "__main__":
    run_tme_engine()
