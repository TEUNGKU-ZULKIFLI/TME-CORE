# ==========================================
# FILE: src/main_engine.py
# FUNGSI: Menggabungkan Jalur A (Deteksi) & Jalur B (Evaluasi Kinerja)
# ==========================================
import re
import time
import datetime
import config.config
from src.api.connection import connect_to_mikrotik, disconnect_from_mikrotik
from src.firewall.mitigator_jalur_a import block_ip

failed_attempts = {}
processed_log_ids = set()
is_first_run = True

def extract_ip(log_message):
    match = re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', log_message)
    return match.group(0) if match else None

def record_performance_data(api, attacker_ip, action_taken):
    """
    JALUR B: Fungsi untuk mencatat data performa (CPU & RAM) 
    ke file log untuk bisa memonitoring Log Activated TME CORE.
    """
    try:
        resources = api.get_resource('/system/resource').get()
        if not resources:
            return
            
        data = resources[0]
        cpu_load = int(data.get('cpu-load', 0))
        free_memory = int(data.get('free-memory', 0)) / (1024 * 1024) # Convert to MB
        total_memory = int(data.get('total-memory', 1)) / (1024 * 1024)
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Format baris data untuk dicatat
        log_line = f"[{timestamp}] IP: {attacker_ip} | Aksi: {action_taken} | CPU: {cpu_load}% | Sisa RAM: {free_memory:.2f}MB / {total_memory:.2f}MB\n"
        
        # Tulis ke file log khusus tmecore
        with open("tmecore.log", "a") as f:
            f.write(log_line)
            
        print(f"[*] DATA EVALUASI DISIMPAN: CPU {cpu_load}% | RAM sisa {free_memory:.2f}MB")
        
    except Exception as e:
        print(f"[-] Gagal merekam data performa: {e}")

def process_engine(api):
    global failed_attempts, processed_log_ids, is_first_run
    
    try:
        logs = api.get_resource('/log').get()
        
        # Skip log lama saat baru dinyalakan
        if is_first_run:
            for log in logs:
                log_id = log.get('id') 
                if log_id: processed_log_ids.add(log_id)
            print(f"[*] Memori disiapkan. Mengabaikan {len(processed_log_ids)} log lama.")
            is_first_run = False
            return
            
        for log in logs:
            log_id = log.get('id')
            message = str(log.get('message', '')).lower()
            
            if log_id in processed_log_ids or not log_id:
                continue
                
            # JALUR A: Deteksi Log
            if "login failure" in message:
                ip_attacker = extract_ip(message)
                
                if ip_attacker:
                    failed_attempts[ip_attacker] = failed_attempts.get(ip_attacker, 0) + 1
                    print(f"[!] DETEKSI: Gagal login dari {ip_attacker} (Gagal ke-{failed_attempts[ip_attacker]})")
                    
                    # JALUR B (Evaluasi Pra-Mitigasi): Catat beban CPU saat serangan sedang berlangsung
                    if failed_attempts[ip_attacker] == config.config.MAX_FAILED_ATTEMPTS - 1:
                         record_performance_data(api, ip_attacker, "SEDANG DISERANG")
                    
                    # JALUR A & B: Ambang batas tercapai, Catat Performa & Blokir!
                    if failed_attempts[ip_attacker] >= config.config.MAX_FAILED_ATTEMPTS:
                        print(f"[>>>] THRESHOLD TERCAPAI: Melakukan pemblokiran pada {ip_attacker}!")
                        
                        # Eksekusi Pemblokiran
                        sukses = block_ip(api, ip_attacker)
                        
                        if sukses:
                            # JALUR B: Catat beban CPU sesaat setelah diblokir
                            record_performance_data(api, ip_attacker, "BERHASIL DIBLOKIR")
                            del failed_attempts[ip_attacker] 
            
            processed_log_ids.add(log_id)
            
    except Exception as e:
        print(f"[-] Error pada Main Engine: {e}")

if __name__ == "__main__":
    api_conn, pool = connect_to_mikrotik()
    if api_conn:
        print("==================================================")
        print("[-] TME-CORE AKTIF: Deteksi (Jalur A) & Evaluasi (Jalur B)")
        print("==================================================")
        try:
            while True:
                process_engine(api_conn)
                time.sleep(3) # Polling tidak boleh terlalu cepat untuk RB hAP
        except KeyboardInterrupt:
            print("\n[*] Pemantauan dihentikan user.")
        finally:
            disconnect_from_mikrotik(pool)