# ==========================================
# FILE: src/alert/notifier.py
# FUNGSI: Mengirim Notifikasi ke Telegram
# ==========================================
import requests
import config.config

def send_telegram_alert(ip_attacker, cpu_load, sisa_ram):
    """
    Fungsi untuk menembak API Telegram Bot.
    Akan dipanggil oleh Main Engine setelah pemblokiran berhasil.
    """
    # Cek apakah token sudah diisi
    if not config.config.TELEGRAM_TOKEN or not config.config.TELEGRAM_CHAT_ID:
        print("[-] NOTIFIKASI: Batal kirim. Token Telegram belum di-setting di config.config.py")
        return False
        
    # Format Pesan yang akan masuk ke HP kamu
    pesan = (
        f"🚨 <b>TME-CORE ALERT: BRUTE FORCE DIBLOKIR!</b> 🚨\n\n"
        f"🛡️ <b>IP Penyerang:</b> <code>{ip_attacker}</code>\n"
        f"⚙️ <b>Beban CPU Saat Diserang:</b> {cpu_load}%\n"
        f"💾 <b>Sisa RAM:</b> {sisa_ram:.2f} MB\n"
        f"✅ <b>Status:</b> IP telah dimasukkan ke Blacklist Firewall MikroTik."
    )
    
    # URL API Telegram
    url = f"https://api.telegram.org/bot{config.config.TELEGRAM_TOKEN}/sendMessage"
    
    # Payload
    payload = {
        "chat_id": config.config.TELEGRAM_CHAT_ID,
        "text": pesan,
        "parse_mode": "HTML"
    }
    
    try:
        response = requests.post(url, data=payload, timeout=5)
        if response.status_code == 200:
            print("[+] NOTIFIKASI: Pesan peringatan berhasil dikirim ke Telegram!")
            return True
        else:
            print(f"[-] GAGAL NOTIFIKASI: Error dari Telegram -> {response.text}")
            return False
    except Exception as e:
        print(f"[-] GAGAL NOTIFIKASI: Tidak ada koneksi internet / Error -> {e}")
        return False