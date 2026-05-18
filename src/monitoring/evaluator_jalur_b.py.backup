# ==========================================
# FILE: src/monitoring/evaluator_jalur_b.py
# FUNGSI: Jalur B - Analisa Beban Router (CPU/RAM)
# ==========================================
import time
import config.config
from src.api.connection import connect_to_mikrotik, disconnect_from_mikrotik
from src.cli.console import print_banner

def check_router_load(api):
    """
    Mengambil data penggunaan CPU dan Memory dari MikroTik.
    """
    try:
        # Ambil data dari /system/resource
        resources = api.get_resource('/system/resource').get()
        
        if not resources:
            return None
            
        # Ekstrak data mentah
        data = resources[0]
        cpu_load = int(data.get('cpu-load', 0))
        free_memory = int(data.get('free-memory', 0))
        total_memory = int(data.get('total-memory', 1)) # Hindari devide by zero
        
        # Kalkulasi persentase RAM yang terpakai
        used_memory = total_memory - free_memory
        ram_usage_percent = int((used_memory / total_memory) * 100)
        
        # --- LOGIKA JALUR B ---
        print(f"[*] BEBAN ROUTER -> CPU: {cpu_load}% | RAM: {ram_usage_percent}%")
        
        # Jika CPU melonjak drastis akibat Brute Force atau hal mencurigakan
        if cpu_load >= config.config.MAX_CPU_USAGE:
            print(f"[!!!] PERINGATAN JALUR B: CPU Overload ({cpu_load}%)!")
            print("[!] Indikasi serangan masif atau aktivitas anomali sedang terjadi.")
            
            # FITUR SKRIPSI: Cek siapa yang sedang aktif login saat CPU tinggi
            active_users = api.get_resource('/user/active').get()
            if active_users:
                print("    Daftar User yang sedang login saat ini:")
                for u in active_users:
                    print(f"    -> User: {u.get('name')} | IP: {u.get('address')} | Via: {u.get('via')}")
            else:
                print("    Tidak ada user aktif terdeteksi (Kemungkinan murni serangan dari luar).")
                
        return cpu_load, ram_usage_percent
        
    except Exception as e:
        print(f"[-] Error saat membaca system resource: {e}")
        return None, None

# --- Main Program Jalur B ---
if __name__ == "__main__":
    # EKSEKUSI TAMPILAN CLI PERTAMA KALI
    print_banner()
    api_conn, pool = connect_to_mikrotik()
    if api_conn:
        print("[-] TME-CORE (JALUR B) AKTIF: Memonitor Beban Router...")
        try:
            while True:
                check_router_load(api_conn)
                time.sleep(3) # Cek setiap 3 detik
        except KeyboardInterrupt:
            print("\n[*] Pemantauan dihentikan user.")
        finally:
            disconnect_from_mikrotik(pool)
