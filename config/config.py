# =========================================================
# FILE: config/config.py
# FUNGSI: Menarik semua kredensial rahasia yang ada di .env
# =========================================================
import os
from dotenv import load_dotenv

# __file__ = config/config.py -> dirname = config/ -> dirname lagi = TME-CORE/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, '.env')

# Memuat file .env ke dalam sistem operasi Python
if os.path.exists(ENV_PATH):
    load_dotenv(ENV_PATH)
else:
    print("[-] PERINGATAN: File .env tidak ditemukan. Sistem menggunakan nilai default!")

# 1. Kredensial MikroTik (RouterBoard)
MIKROTIK_IP = os.getenv("MIKROTIK_IP")
MIKROTIK_USER = os.getenv("MIKROTIK_USER")
MIKROTIK_PASS = os.getenv("MIKROTIK_PASS")
MIKROTIK_PORT = int(os.getenv("MIKROTIK_PORT", 8728))

# 2. Threshold JALUR A (Pola Login)
MAX_FAILED_ATTEMPTS = 5       
BLOCK_TIMEOUT = "1h"          
ADDRESS_LIST_NAME = "brute_force_block"

# DAFTAR IP ADMIN/SERVER YANG KEBAL BLOKIR (Tidak akan pernah diblokir)
# Tambahkan IP Debian kamu atau IP Laptop Windows kamu di sini
whitelist_str = os.getenv("WHITELIST_IPS")
WHITELIST_IPS = [ip.strip() for ip in whitelist_str.split(',')]

# 3. Threshold JALUR B (Beban Router)
MAX_CPU_USAGE = 80            # Batas toleransi CPU (%) sebelum alarm berbunyi
MAX_RAM_USAGE = 90            # Batas toleransi RAM (%) (Opsional)

# 4. Kredensial Bot Telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# 5. Konfigurasi Direktori Log Evaluasi Skripsi
DATA_DIR = os.path.join(BASE_DIR, "data")
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

LOG_FILE_PATH = os.path.join(DATA_DIR, "tmecore.log")
