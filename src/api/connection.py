import routeros_api
from config.config import MIKROTIK_IP, MIKROTIK_USER, MIKROTIK_PASS, MIKROTIK_PORT

def connect_to_mikrotik(quiet=False):
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
    if connection_pool:
        try:
            connection_pool.disconnect()
        except Exception:
            pass
        if not quiet:
            print("[*] Koneksi ke MikroTik ditutup dengan aman.")
