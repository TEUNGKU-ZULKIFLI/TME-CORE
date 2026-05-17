# ==========================================
# FILE: src/detection/detector_jalur_a.py
# FUNGSI: Jalur A - Mendeteksi log Brute Force
# ==========================================
import re
import time
import config.config
from src.api.connection import connect_to_mikrotik, disconnect_from_mikrotik
from src.firewall.mitigator_jalur_a import block_ip

failed_attempts = {}
processed_log_ids = set()
is_first_run = True  # Flag agar log lama tidak langsung diblokir saat script baru nyala

def extract_ip(log_message):
    match = re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', log_message)
    return match.group(0) if match else None

def process_logs(api):
    global failed_attempts, processed_log_ids, is_first_run
    
    try:
        logs = api.get_resource('/log').get()
        
        # Jika baru pertama kali nyala, cukup catat ID-nya saja (Skip processing)
        if is_first_run:
            for log in logs:
                log_id = log.get('id') 
                if log_id:
                    processed_log_ids.add(log_id)
            print(f"[*] Memori disiapkan. Mengabaikan {len(processed_log_ids)} log lama.")
            is_first_run = False
            return
            
        # Untuk proses selanjutnya (Deteksi Real-Time)
        for log in logs:
            log_id = log.get('id')
            message = str(log.get('message', '')).lower()
            
            # Jika log sudah pernah diproses, lewati
            if log_id in processed_log_ids or not log_id:
                continue
                
            # Filter log Brute Force
            if "login failure" in message:
                ip_attacker = extract_ip(message)
                
                if ip_attacker:
                    failed_attempts[ip_attacker] = failed_attempts.get(ip_attacker, 0) + 1
                    print(f"[!] DETEKSI: Gagal login dari {ip_attacker} (Gagal ke-{failed_attempts[ip_attacker]})")
                    
                    # Jika mencapai threshold
                    if failed_attempts[ip_attacker] >= config.config.MAX_FAILED_ATTEMPTS:
                        print(f"[>>>] THRESHOLD TERCAPAI: Melakukan pemblokiran pada {ip_attacker}!")
                        
                        # ---> EKSEKUSI JALUR A (MITIGASI) <---
                        sukses = block_ip(api, ip_attacker)
                        
                        if sukses:
                            # Hapus dari memori agar perhitungan dimulai dari 0 lagi jika timeout blokir habis
                            del failed_attempts[ip_attacker] 
            
            # Tandai log ini sudah dibaca
            processed_log_ids.add(log_id)
            
    except Exception as e:
        print(f"[-] Error saat membaca log: {e}")

# --- Main Program Jalur A ---
if __name__ == "__main__":
    api_conn, pool = connect_to_mikrotik()
    if api_conn:
        print("[-] TME-CORE (JALUR A) AKTIF: Menunggu serangan masuk...")
        try:
            while True:
                process_logs(api_conn)
                time.sleep(2) # Polling lebih cepat (2 detik)
        except KeyboardInterrupt:
            print("\n[*] Pemantauan dihentikan user.")
        finally:
            disconnect_from_mikrotik(pool)