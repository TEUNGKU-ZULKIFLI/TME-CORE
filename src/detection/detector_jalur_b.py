# =================================================================
# FILE: src/detection/detector_jalur_b.py
# FUNGSI: Deteksi Anomali Jalur B - Brute Force Success Prevention
# =================================================================
import datetime
from config import config
from src.firewall.mitigator_jalur_a import block_ip
from src.alert.notifier import send_telegram_alert

def check_active_session_anomalies(api, failed_attempts, session_blocked_ips):
    """
    Memeriksa sesi aktif di MikroTik (/user/active) dan mencocokkannya 
    dengan riwayat kegagalan login di memori TME-CORE.
    Jika IP yang aktif memiliki catatan kegagalan > 0, sesi akan diputus paksa dan IP diblokir.
    """
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
                
            # Abaikan jika IP sudah terblokir sebelumnya
            if ip_clean in session_blocked_ips:
                continue
                
            # 2. DETEKSI ANOMALI:
            # Jika IP tersebut terdaftar aktif login, namun memiliki riwayat gagal login sebelumnya
            if ip_clean in failed_attempts and failed_attempts[ip_clean] > 0:
                print(f"\033[91m[🚨 ANOMALI DETECTED]: IP {ip_clean} berhasil masuk sebagai '{username}' via {via_service}")
                print(f"                       setelah mengalami {failed_attempts[ip_clean]} kegagalan!\033[0m")
                
                # A. Eksekusi Pemutusan Sesi Paksa (Forced Session Termination)
                api.get_resource('/user/active').remove(id=session_id)
                print(f"[+] MITIGASI JALUR B: Sesi aktif {ip_clean} telah diputus paksa (Terminated).")
                
                # B. Eksekusi Pemblokiran Permanen
                sukses_blokir = block_ip(api, ip_clean)
                
                if sukses_blokir:
                    session_blocked_ips.add(ip_clean)
                    
                    # C. Kirim Notifikasi Telegram Khusus Anomali
                    pesan_alert = (
                        f"🚨 <b>TME-CORE ANOMALY ALERT</b>\n"
                        f"───────────────────────────\n"
                        f"📌 <b>IP Penyerang</b> : {ip_clean}\n"
                        f"🔑 <b>Username</b>    : {username}\n"
                        f"🛡️ <b>Status</b>      : BERHASIL LOGIN BYPASS (Anomali)\n"
                        f"⚡ <b>Aksi Mitigasi</b>: SESSION KICK & BLACKLIST DROP\n"
                        f"📈 <b>Riwayat Gagal</b> : {failed_attempts[ip_clean]} kali\n"
                        f"───────────────────────────\n"
                        f"📅 Dilaporkan secara real-time oleh Jalur B Engine"
                    )
                    
                    # Gunakan bot telegram untuk mengirim pesan
                    send_telegram_alert(ip_clean, 100, 8.0, custom_message=pesan_alert)
                    
                    # Hapus dari memori gagal login
                    del failed_attempts[ip_clean]
                    return True
                    
    except Exception as e:
        print(f"[-] ERROR JALUR B DETECTOR: {e}")
        
    return False