# ==========================================
# FILE: src/main_engine.py
# FUNGSI: Orkestrator Utama TME-CORE
# ==========================================
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

import re
import time
import datetime
from config import config
from src.api.connection import connect_to_mikrotik, disconnect_from_mikrotik
from src.firewall.mitigator_jalur_a import block_ip
from src.alert.notifier import send_telegram_alert
from src.cli.console import print_banner, run_doctor
from src.monitoring.evaluator_jalur_b import record_performance_to_csv
from src.db.state_manager import load_state, save_state

failed_attempts, session_blocked_ips = load_state()
processed_log_ids = set()
is_first_run = True
last_cpu = 0
last_ram = 0

def extract_ip(log_message):
    match = re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', log_message)
    return match.group(0) if match else None

def write_system_log(message):
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_dir = os.path.dirname(config.SYSTEM_LOG_PATH)
        os.makedirs(log_dir, exist_ok=True)
        with open(config.SYSTEM_LOG_PATH, "a") as f:
            f.write(f"[{timestamp}] {message}\n")
    except Exception:
        pass

def process_engine(api):
    global failed_attempts, processed_log_ids, is_first_run, last_cpu, last_ram, session_blocked_ips

    try:
        logs = api.get_resource('/log').get()

        if is_first_run:
            for log in logs:
                log_id = log.get('id')
                if log_id: processed_log_ids.add(log_id)
            print(f"[*] Memori disiapkan. Mengabaikan {len(processed_log_ids)} log lama.")
            write_system_log(f"Sistem dimulai. Mengabaikan {len(processed_log_ids)} log lama.")
            is_first_run = False
            return

        for log in logs:
            log_id = log.get('id')
            message = str(log.get('message', '')).lower()

            if log_id in processed_log_ids or not log_id: continue

            if "login failure" in message:
                ip_attacker = extract_ip(message)

                if ip_attacker:
                    if ip_attacker in session_blocked_ips:
                        processed_log_ids.add(log_id)
                        continue

                    if ip_attacker in config.WHITELIST_IPS:
                        print(f"[-] ABAIKAN: IP {ip_attacker} (Admin) dilindungi Whitelist.")
                        write_system_log(f"Aktivitas gagal login dari Whitelist IP: {ip_attacker} diabaikan.")
                        processed_log_ids.add(log_id)
                        continue

                    failed_attempts[ip_attacker] = failed_attempts.get(ip_attacker, 0) + 1
                    print(f"[!] DETEKSI: Gagal login dari {ip_attacker} (Gagal ke-{failed_attempts[ip_attacker]})")

                    save_state(failed_attempts, session_blocked_ips)

                    if failed_attempts[ip_attacker] == config.MAX_FAILED_ATTEMPTS - 1:
                         cpu, ram = record_performance_to_csv(api, ip_attacker, "SEDANG DISERANG")
                         if cpu is not None:
                             last_cpu = cpu
                             last_ram = ram

                    if failed_attempts[ip_attacker] >= config.MAX_FAILED_ATTEMPTS:
                        print(f"\033[91m[>>>] THRESHOLD TERCAPAI: Melakukan pemblokiran pada {ip_attacker}!\033[0m")
                        write_system_log(f"Serangan brute force terdeteksi dari IP {ip_attacker}. Memicu aksi blokir.")

                        sukses = block_ip(api, ip_attacker)

                        if sukses:
                            cpu, ram = record_performance_to_csv(api, ip_attacker, "BERHASIL DIBLOKIR")
                            if cpu is not None:
                                last_cpu = cpu
                                last_ram = ram

                            print("[*] Mengirim 1x laporan ke Telegram...")
                            send_telegram_alert(ip_attacker, last_cpu, last_ram)

                            session_blocked_ips.add(ip_attacker)
                            del failed_attempts[ip_attacker]

                            save_state(failed_attempts, session_blocked_ips)

            processed_log_ids.add(log_id)

    except Exception as e:
        print(f"[-] Error pada Main Engine: {e}")
        write_system_log(f"ENGINE ERROR: {e}")

if __name__ == "__main__":
    print_banner()
    run_doctor(config.ENV_PATH, config.DATA_DIR, config)

    print("\033[93m[*] Mencoba koneksi ke RouterOS MikroTik...\033[0m")
    api_conn, pool = connect_to_mikrotik()
    if api_conn:
        print(f"\033[92m[+] TME-CORE Engine siap menahan serangan!\033[0m")
        write_system_log("Koneksi API sukses. TME-CORE aktif.")
        print("=" * 65)
        try:
            while True:
                process_engine(api_conn)
                time.sleep(3)
        except KeyboardInterrupt:
            print("\n\033[93m[*] Proses dihentikan oleh user (Ctrl+C).\033[0m")
            write_system_log("Sistem dihentikan manual oleh Administrator.")
        finally:
            disconnect_from_mikrotik(pool)
