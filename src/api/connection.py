# ==========================================
# FILE: connection.py
# FUNGSI: Jembatan komunikasi ke RouterOS
# ==========================================
import routeros_api
import config.config

def connect_to_mikrotik():
    """
    Fungsi ini bertugas membuka jalur API ke MikroTik.
    Return: object koneksi (api) jika sukses, None jika gagal.
    """
    try:
        # Inisialisasi parameter koneksi
        connection = routeros_api.RouterOsApiPool(
            config.config.MIKROTIK_IP,
            username=config.config.MIKROTIK_USER,
            password=config.config.MIKROTIK_PASS,
            port=config.config.MIKROTIK_PORT,
            plaintext_login=True
        )
        
        # Eksekusi koneksi
        api = connection.get_api()
        print(f"[+] SUKSES: Terhubung ke MikroTik {config.config.MIKROTIK_IP}")
        return api, connection
        
    except Exception as e:
        print(f"[-] GAGAL KONEKSI: Pastikan API MikroTik aktif (/ip services enable api)")
        print(f"[-] Error Log: {e}")
        return None, None

def disconnect_from_mikrotik(connection_pool):
    """
    Fungsi untuk menutup koneksi agar CPU MikroTik tidak penuh (Memory Leak)
    """
    if connection_pool:
        connection_pool.disconnect()
        print("[*] Koneksi ke MikroTik ditutup dengan aman.")

# --- Blok Testing (Hanya jalan jika file ini dieksekusi langsung) ---
if __name__ == "__main__":
    print("Mencoba koneksi ke MikroTik...")
    api_conn, pool = connect_to_mikrotik()
    if api_conn:
        disconnect_from_mikrotik(pool)
