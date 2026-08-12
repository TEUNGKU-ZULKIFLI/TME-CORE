# ==========================================
# FILE: src/api/connection.py
# FUNGSI: Jembatan komunikasi ke RouterOS
# ==========================================
from config.config import MIKROTIK_IP, MIKROTIK_USER, MIKROTIK_PASS, MIKROTIK_PORT
import routeros_api
from src.cli.console import print_banner


def connect_to_mikrotik():
    try:
        # Inisialisasi parameter koneksi menggunakan kredensial dari config
        connection = routeros_api.RouterOsApiPool(
            MIKROTIK_IP,
            username=MIKROTIK_USER,
            password=MIKROTIK_PASS,
            port=MIKROTIK_PORT,
            plaintext_login=True,
        )

        api = connection.get_api()
        print(f"[✓] SUKSES: Terhubung ke MikroTik {MIKROTIK_IP}")
        return api, connection

    except Exception as e:
        # Lebih informatif tentang alasan kegagalan koneksi
        print("[✗] GAGAL KONEKSI: Pastikan API MikroTik aktif (/ip service enable api) dan kredensial benar.")
        print(f"[✗] Error Log: {e}")
        return None, None


def disconnect_from_mikrotik(connection_pool):
    if connection_pool:
        try:
            connection_pool.disconnect()
        except Exception:
            pass
        print("[*] Koneksi ke MikroTik ditutup dengan aman.")


# --- Blok Testing (Hanya jalan jika file ini dieksekusi langsung) ---
if __name__ == "__main__":
    print_banner()
    print("Mencoba koneksi ke MikroTik...")
    api_conn, pool = connect_to_mikrotik()
    if api_conn:
        disconnect_from_mikrotik(pool)
