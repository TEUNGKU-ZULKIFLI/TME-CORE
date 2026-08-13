# =========================================================
# FILE: src/db/state_manager.py
# FUNGSI: Ingatan Permanen (State Persistence) TME-CORE
# =========================================================
import json
import os
import datetime
from config.config import STATE_DB_PATH, MAX_FAILED_ATTEMPTS, STATE_RETENTION_SECONDS

def load_state():
    """
    Membaca database state JSON dari disk dan merestore ingatan sistem.
    """
    if not os.path.exists(STATE_DB_PATH):
        print(f"[*] Database: File belum ditemukan ({STATE_DB_PATH}). Memulai dengan state baru.")
        return {}, set(), {}, 0, 0

    try:
        with open(STATE_DB_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)

        raw_failed = data.get("failed_attempts", {})

        # Normalisasi failed_attempts ke format list of timestamps
        failed_attempts = {}
        for k, v in raw_failed.items():
            if isinstance(v, list):
                failed_attempts[k] = v
            else:
                failed_attempts[k] = []

        blocked_ips_list = data.get("session_blocked_ips", [])
        session_blocked_ips = set(blocked_ips_list)

        # Persistent counts (bertahan meskipun service direstart)
        persistent_failed_counts = data.get("persistent_failed_counts", {})
        normalized_pfc = {}
        for ip, entry in persistent_failed_counts.items():
            if isinstance(entry, dict):
                cnt = int(entry.get('count', 0))
                last = float(entry.get('last', 0))
                normalized_pfc[ip] = {'count': cnt, 'last': last}
            elif isinstance(entry, int):
                normalized_pfc[ip] = {'count': int(entry), 'last': 0}
            else:
                normalized_pfc[ip] = {'count': 0, 'last': 0}

        total_attacks_detected = data.get("total_attacks_detected", 0)
        total_attacks_blocked = data.get("total_attacks_blocked", 0)

        # Cetak laporan pemulihan state secara ringkas
        num_failed_ips = len(failed_attempts)
        num_blocked_ips = len(session_blocked_ips)

        print(f"\n[✓] DATABASE RESTORED ({STATE_DB_PATH}):")
        print(f"    ├─ IP Percobaan Login Gagal : {num_failed_ips}")
        print(f"    ├─ IP Terblokir di Firewall : {num_blocked_ips}")
        print(f"    ├─ Total Serangan Terdeteksi: {total_attacks_detected}")
        print(f"    └─ Total Serangan Terblokir : {total_attacks_blocked}\n")

        return failed_attempts, session_blocked_ips, normalized_pfc, total_attacks_detected, total_attacks_blocked

    except json.JSONDecodeError as e:
        print(f"[-] DATABASE ERROR: File JSON korup ({STATE_DB_PATH}) -> {e}")
        print(f"[!] Memulai dengan state kosong.\n")
        return {}, set(), {}, 0, 0
    except Exception as e:
        print(f"[-] DATABASE ERROR: Gagal membaca {STATE_DB_PATH} -> {e}")
        print(f"[!] Memulai dengan state kosong.\n")
        return {}, set(), {}, 0, 0


def save_state(failed_attempts, session_blocked_ips, persistent_failed_counts=None, total_attacks_detected=0, total_attacks_blocked=0):
    """
    Menyimpan state terkini ke dalam berkas JSON secara sinkron.
    """
    try:
        if persistent_failed_counts is None:
            persistent_failed_counts = {}

        data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "failed_attempts": failed_attempts,
            "session_blocked_ips": list(session_blocked_ips),
            "persistent_failed_counts": persistent_failed_counts,
            "total_attacks_detected": total_attacks_detected,
            "total_attacks_blocked": total_attacks_blocked
        }
        os.makedirs(os.path.dirname(STATE_DB_PATH), exist_ok=True)
        with open(STATE_DB_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"[-] DATABASE ERROR: Gagal menyimpan state -> {e}")


# --- Blok Testing Mandiri ---
if __name__ == "__main__":
    print("=== TESTING MODUL STATE MANAGER ===")
    
    # 1. Tes Simpan State Dummy
    dummy_failed = {"192.168.20.99": [1700000000.0]}
    dummy_blocked = {"192.168.20.99"}
    dummy_pfc = {"192.168.20.99": {'count': 3, 'last': 1700000000.0}}
    
    print("[*] Menyimpan state uji coba...")
    save_state(dummy_failed, dummy_blocked, dummy_pfc, total_attacks_detected=1, total_attacks_blocked=1)
    
    # 2. Tes Membaca State kembali
    print("[*] Membaca state dari disk...")
    load_state()
