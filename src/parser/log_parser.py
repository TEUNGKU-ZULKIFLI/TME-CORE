# ==========================================
# FILE: parser/log_parser.py
# FUNGSI: Pengecekan Raw Data Log MikroTik
# ==========================================
import config.config
from src.api.connection import connect_to_mikrotik, disconnect_from_mikrotik

api, pool = connect_to_mikrotik()
if api:
    print("\n[*] Mengambil raw data log dari API MikroTik...")
    # Tarik semua data di menu /log
    logs = api.get_resource('/log').get()

    print(f"[*] Jumlah total log di memory MikroTik saat ini: {len(logs)}")
    print("\n=== 5 RAW LOG TERAKHIR ===")

    # Print 5 log terbawah untuk melihat struktur datanya
    for log in logs[-5:]:
        print(log)

    print("==========================\n")
    disconnect_from_mikrotik(pool)
