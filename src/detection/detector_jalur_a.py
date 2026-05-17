# ==========================================
# FILE: src/detection/detector_jalur_a.py
# FUNGSI: Jalur A - Mendeteksi log Brute Force
# ==========================================
import re
import time
import config.config
from src.api.connection import connect_to_mikrotik, disconnect_from_mikrotik

failed_attempts = {}
processed_log_ids = set()

def extract_ip(log_message):
    match = re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', log_message)
    return match.group(0) if match else None

def get_bruteforce_attackers(api):
    global failed_attempts, processed_log_ids
    attackers_to_block = []
    
    try:
        logs = api.get_resource('/log').get()
        print(f"[*] [DEBUG] Mengambil {len(logs)} log dari MikroTik...")
        
        for log in logs:
            log_id = log.get('id')
            # Gunakan get dan pastikan string dengan format lower()
            message = str(log.get('message', '')).lower()
            topics = str(log.get('topics', '')).lower()
            
            if log_id in processed_log_ids:
                continue
                
            # Filter log: Cari kata "login failure" di message
            if "login failure" in message:
                ip_attacker = extract_ip(message)
                
                if ip_attacker:
                    failed_attempts[ip_attacker] = failed_attempts.get(ip_attacker, 0) + 1
                    print(f"[!] DETEKSI: Gagal login dari {ip_attacker} (Total: {failed_attempts[ip_attacker]}x) | ID: {log_id}")
                    
                    if failed_attempts[ip_attacker] >= config.config.MAX_FAILED_ATTEMPTS:
                        print(f"[>>>] THRESHOLD TERCAPAI: IP {ip_attacker} siap dikirim ke modul blokir!")
                        attackers_to_block.append(ip_attacker)
                        failed_attempts[ip_attacker] = 0 
            
            processed_log_ids.add(log_id)
            
        return attackers_to_block
        
    except Exception as e:
        print(f"[-] Error saat membaca log: {e}")
        return []

if __name__ == "__main__":
    api_conn, pool = connect_to_mikrotik()
    if api_conn:
        print("[-] Memulai pemantauan log (Mode Verbose)...")
        try:
            while True:
                attackers = get_bruteforce_attackers(api_conn)
                if attackers:
                    print(f"[#] AKSI JALUR A: Siapkan script pemblokiran untuk IP {attackers}")
                time.sleep(3) # Jeda 3 detik
        except KeyboardInterrupt:
            print("\n[*] Pemantauan dihentikan user.")
        finally:
            disconnect_from_mikrotik(pool)
