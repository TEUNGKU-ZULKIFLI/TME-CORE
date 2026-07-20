# ==========================================
# FILE: src/alert/notifier.py
# FUNGSI: Mengirim Notifikasi ke Telegram
# ==========================================
import requests
from config import config

def send_telegram_alert(ip_attacker, cpu_load, sisa_ram, service="SSH (Port 22)", adr=100.0, custom_message=None):
    """
    Mengirimkan pesan peringatan mitigasi otomatis dengan visualisasi
    yang kontras dan terstruktur menggunakan parsing HTML.
    Mendukung info PORT layanan yang diserang dan nilai ADR sistem.
    Mendukung pengiriman pesan kustom untuk anomali Jalur B.
    """
    if not config.TELEGRAM_TOKEN or not config.TELEGRAM_CHAT_ID:
        print("[-] NOTIFIKASI: Token Telegram atau Chat ID belum dikonfigurasi.")
        return False

    # Jika ada pesan kustom (seperti alert anomali Jalur B), langsung gunakan pesan tersebut
    if custom_message:
        pesan = custom_message
    else:
        # Desain visualisasi indikator beban CPU menggunakan Emoji Meter
        cpu_bar = "🟢"
        if cpu_load >= 80:
            cpu_bar = "🔴 (CRITICAL)"
        elif cpu_load >= 50:
            cpu_bar = "🟡 (WARNING)"

        # Format Pesan HTML yang Estetis (Default)
        pesan = (
            f"<b>🛡️ TME-CORE SYSTEM ALERT</b>\n"
            f"<i>Automated Intrusion Prevention Active</i>\n"
            f"───────────────────────────\n\n"
            f"🚨 <b>SERANGAN BRUTE FORCE DIBLOKIR!</b>\n"
            f"📌 <b>IP Penyerang :</b> <code>{ip_attacker}</code>\n"
            f"🌐 <b>Layanan/Port  :</b> <code>{service}</code>\n"
            f"⚡ <b>Status Aksi   :</b> <code>DROP (Blacklisted)</code>\n"
            f"🎯 <b>Sistem ADR    :</b> <code>{adr:.1f}%</code>\n\n"
            f"📊 <b>METRIK SUMBER DAYA ROUTER:</b>\n"
            f"  ├─ Beban CPU : {cpu_load}% {cpu_bar}\n"
            f"  └─ Sisa RAM  : {sisa_ram:.2f} MB / 32.00 MB\n\n"
            f"───────────────────────────\n"
            f"📅 <i>Dilaporkan secara real-time oleh TME Engine</i>"
        )

    url = f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": config.TELEGRAM_CHAT_ID,
        "text": pesan,
        "parse_mode": "HTML"
    }

    try:
        response = requests.post(url, data=payload, timeout=5)
        if response.status_code == 200:
            print("[+] NOTIFIKASI: Pesan peringatan berhasil dikirim ke Telegram!")
            return True
        else:
            print(f"[-] GAGAL NOTIFIKASI: Telegram API Return -> {response.text}")
            return False
    except Exception as e:
        print(f"[-] GAGAL NOTIFIKASI: Masalah koneksi jaringan ke API Telegram -> {e}")
        return False
