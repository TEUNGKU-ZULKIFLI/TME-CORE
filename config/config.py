# =========================================================
# FILE: config/config.py
# FUNGSI: Menarik semua kredensial rahasia yang ada di .env
# =========================================================
import os
from dotenv import load_dotenv

# Path Root TME-CORE
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, '.env')

if os.path.exists(ENV_PATH):
    load_dotenv(ENV_PATH)
else:
    print("[-] PERINGATAN: File .env tidak ditemukan. Menggunakan nilai default!")

# 1. Kredensial MikroTik
MIKROTIK_IP = os.getenv("MIKROTIK_IP", "192.168.10.1")
MIKROTIK_USER = os.getenv("MIKROTIK_USER", "admin")
MIKROTIK_PASS = os.getenv("MIKROTIK_PASS", "")
MIKROTIK_PORT = int(os.getenv("MIKROTIK_PORT", 8728))

# 2. Whitelist
whitelist_str = os.getenv("WHITELIST_IPS", "127.0.0.1")
WHITELIST_IPS = [ip.strip() for ip in whitelist_str.split(',')]

# 3. Kredensial Telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# 4. Parameter Threshold
MAX_FAILED_ATTEMPTS = 5 # Disesuaikan dengan pengujian standar
BLOCK_TIMEOUT = "24h"
ADDRESS_LIST_NAME = "brute_force_block"
MAX_CPU_USAGE = 80
MAX_RAM_USAGE = 90

# 5. Konfigurasi Path dan Direktori
DATA_DIR = os.path.join(BASE_DIR, "data")
STATE_RETENTION_SECONDS = int(os.getenv("STATE_RETENTION_SECONDS", 3600))
DB_DIR = os.path.join(DATA_DIR, "db")
LOGS_DIR = os.path.join(DATA_DIR, "logs")
METRICS_DIR = os.path.join(DATA_DIR, "metrics")
SAMPLES_DIR = os.path.join(DATA_DIR, "samples")

# Otomatis membuat semua folder jika belum ada (Lebih aman dari race condition)
for directory in [DATA_DIR, DB_DIR, LOGS_DIR, METRICS_DIR, SAMPLES_DIR]:
    os.makedirs(directory, exist_ok=True)

# Output Paths File Spesifik
SYSTEM_LOG_PATH = os.path.join(LOGS_DIR, "tmecore_system.log")
METRICS_CSV_PATH = os.path.join(METRICS_DIR, "evaluasi_kinerja.csv")
STATE_DB_PATH = os.path.join(DB_DIR, "tme_state.json")
