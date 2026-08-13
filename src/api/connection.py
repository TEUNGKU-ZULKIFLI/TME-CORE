# ==========================================
# FILE: src/api/connection.py
# FUNGSI: Jembatan komunikasi ke RouterOS
# ==========================================
from config.config import MIKROTIK_IP, MIKROTIK_USER, MIKROTIK_PASS, MIKROTIK_PORT
import routeros_api

def connect_to_mikrotik(quiet=False):
    """
    Membangun koneksi ke API MikroTik.
    :param quiet: Jika True, tidak akan mencetak log sukses (menghindari spam di loop).
    """
    try:
        connection = routeros_api.RouterOsApiPool(
            MIKROTIK_IP,
            username=MIKROTIK_USER,
            password=MIKROTIK_PASS,
            port=MIKROTIK_PORT,
            plaintext_login=True,
        )

        api = connection.get_api()
        if not quiet:
            print(f"[✓] SUKSES: Terhubung ke MikroTik {MIKROTIK_IP}")
        return api, connection

    except Exception as e:
        print("[✗] GAGAL KONEKSI: Pastikan API MikroTik aktif (/ip service enable api) dan kredensial benar.")
        print(f"[✗] Error Log: {e}")
        return None, None


def disconnect_from_mikrotik(connection_pool, quiet=False):
    """
    Menutup koneksi dari MikroTik.
    """
    if connection_pool:
        try:
            connection_pool.disconnect()
        except Exception:
            pass
        
        if not quiet:
            print("[*] Koneksi ke MikroTik ditutup dengan aman.")


# --- Blok Testing Mandiri ---
if __name__ == "__main__":
    try:
        from src.cli.console import print_banner
        print_banner()
    except ImportError:
        print("=== MIKROTIK API CONNECTION TEST ===")
        
    print("Mencoba koneksi ke MikroTik...")
    api_conn, pool = connect_to_mikrotik(quiet=False)
    
    if api_conn:
        # Coba jalankan 1 command ringan untuk memastikan API merespon
        identity = api_conn.get_resource('/system/identity').get()
        print(f"[*] Identitas Router: {identity[0]['name']}")
        
        disconnect_from_mikrotik(pool, quiet=False)
