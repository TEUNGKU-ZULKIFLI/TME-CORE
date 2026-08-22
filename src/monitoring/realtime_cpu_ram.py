# ==========================================
# FILE: src/monitoring/realtime_cpu_ram.py
# FUNGSI: Monitoring Realtime CPU dan Memory dari MikroTik
# ==========================================
import time
from typing import Tuple, Optional
from config.config import MAX_CPU_USAGE

def check_router_load(api) -> Tuple[Optional[int], Optional[int]]:
    """
    Mengecek penggunaan CPU dan RAM dari MikroTik secara realtime.
    """
    try:
        resources = api.get_resource('/system/resource').get()

        if not resources:
            return None, None

        data = resources[0]
        cpu_load = int(data.get('cpu-load', 0))
        free_memory = int(data.get('free-memory', 0))
        total_memory = int(data.get('total-memory', 1))

        used_memory = total_memory - free_memory
        ram_usage_percent = int((used_memory / total_memory) * 100)

        print(f"[*] BEBAN ROUTER -> CPU: {cpu_load}% | RAM: {ram_usage_percent}%")

        if cpu_load >= MAX_CPU_USAGE:
            print(f"[!!!] PERINGATAN: CPU Overload ({cpu_load}%)!")
            print("[!] Indikasi serangan masif atau aktivitas anomali sedang terjadi.")

            try:
                active_users = api.get_resource('/user/active').get()
                if active_users:
                    print("    Daftar User yang sedang login saat ini:")
                    for u in active_users:
                        print(f"    -> User: {u.get('name')} | IP: {u.get('address')} | Via: {u.get('via')}")
                else:
                    print("    Tidak ada user aktif terdeteksi.")
            except Exception:
                pass

        return cpu_load, ram_usage_percent

    except Exception as e:
        print(f"[✗] Error saat membaca system resource: {e}")
        return None, None


# --- Blok Testing Mandiri ---
if __name__ == "__main__":
    from src.cli.console import print_banner
    from src.api.connection import connect_to_mikrotik, disconnect_from_mikrotik

    print_banner()
    api_conn, pool = connect_to_mikrotik()
    if api_conn:
        print("[!] TME-CORE REAL TIME AKTIF: Memonitor Beban Router (Tekan Ctrl+C untuk berhenti)...")
        try:
            for _ in range(60): # Cek 60 kali dalam pengujian mandiri
                check_router_load(api_conn)
                time.sleep(2)
        except KeyboardInterrupt:
            print("\n[*] Pemantauan dihentikan user.")
        finally:
            disconnect_from_mikrotik(pool)
