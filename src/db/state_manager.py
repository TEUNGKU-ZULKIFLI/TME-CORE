# =========================================================
# FILE: src/db/state_manager.py
# FUNGSI: Ingatan Permanen (State Persistence) TME-CORE
# =========================================================
import json
import os
import config.config

def load_state():
    """
    Membaca ingatan TME-CORE dari file JSON saat sistem pertama kali menyala.
    Mengembalikan 2 nilai: failed_attempts (dict) dan session_blocked_ips (set).
    """
    if not os.path.exists(config.config.STATE_DB_PATH):
        # Jika belum ada database, kembalikan data kosong
        return {}, set()

    try:
        with open(config.config.STATE_DB_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)

            # Ambil data failed_attempts, default {} jika tidak ada
            failed_attempts = data.get("failed_attempts", {})

            # Ambil data blocked_ips, ubah kembali dari list menjadi set
            blocked_ips_list = data.get("session_blocked_ips", [])
            session_blocked_ips = set(blocked_ips_list)

            print(f"[+] DATABASE: Berhasil memuat ingatan. ({len(session_blocked_ips)} IP Terblokir di memori)")
            return failed_attempts, session_blocked_ips

    except Exception as e:
        print(f"[-] DATABASE ERROR: Gagal membaca {config.config.STATE_DB_PATH} -> {e}")
        return {}, set()

def save_state(failed_attempts, session_blocked_ips):
    """
    Menyimpan kondisi terkini ke file JSON.
    Dipanggil setiap kali ada perubahan jumlah gagal login atau blokir.
    """
    try:
        # JSON tidak mendukung tipe data 'set', jadi kita ubah jadi 'list' dulu
        data = {
            "failed_attempts": failed_attempts,
            "session_blocked_ips": list(session_blocked_ips)
        }

        # Pastikan folder db/ ada
        os.makedirs(os.path.dirname(config.config.STATE_DB_PATH), exist_ok=True)

        with open(config.config.STATE_DB_PATH, 'w', encoding='utf-8') as f:
            # indent=4 agar file JSON nya rapi dan mudah dibaca manusia
            json.dump(data, f, indent=4)

    except Exception as e:
        pass # Diamkan saja jika error agar tidak mengganggu proses utama
