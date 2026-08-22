import json
import os
import datetime
from config.config import STATE_DB_PATH

def load_state():
    if not os.path.exists(STATE_DB_PATH):
        print(f"[*] Database: File belum ditemukan ({STATE_DB_PATH}). Memulai dengan state baru.")
        return {}, set(), {}, 0, 0

    try:
        with open(STATE_DB_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)

        raw_failed = data.get("failed_attempts", {})
        failed_attempts = {k: v if isinstance(v, list) else [] for k, v in raw_failed.items()}

        session_blocked_ips = set(data.get("session_blocked_ips", []))
        
        persistent_failed_counts = data.get("persistent_failed_counts", {})
        normalized_pfc = {}
        for ip, entry in persistent_failed_counts.items():
            if isinstance(entry, dict):
                normalized_pfc[ip] = {'count': int(entry.get('count', 0)), 'last': float(entry.get('last', 0))}
            elif isinstance(entry, int):
                normalized_pfc[ip] = {'count': int(entry), 'last': 0.0}
            else:
                normalized_pfc[ip] = {'count': 0, 'last': 0.0}

        total_attacks_detected = data.get("total_attacks_detected", 0)
        total_attacks_blocked = data.get("total_attacks_blocked", 0)

        print(f"\n[✓] DATABASE RESTORED ({STATE_DB_PATH}):")
        print(f"    ├─ IP Percobaan Login Gagal : {len(failed_attempts)}")
        print(f"    ├─ IP Terblokir di Firewall : {len(session_blocked_ips)}")
        print(f"    ├─ Total Serangan Terdeteksi: {total_attacks_detected}")
        print(f"    └─ Total Serangan Terblokir : {total_attacks_blocked}\n")

        return failed_attempts, session_blocked_ips, normalized_pfc, total_attacks_detected, total_attacks_blocked

    except (json.JSONDecodeError, Exception) as e:
        print(f"[-] DATABASE ERROR: Gagal membaca/parsing state ({STATE_DB_PATH}) -> {e}")
        print(f"[!] Memulai dengan state kosong.\n")
        return {}, set(), {}, 0, 0


def save_state(failed_attempts, session_blocked_ips, persistent_failed_counts=None, total_attacks_detected=0, total_attacks_blocked=0):
    try:
        data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "failed_attempts": failed_attempts,
            "session_blocked_ips": list(session_blocked_ips),
            "persistent_failed_counts": persistent_failed_counts or {},
            "total_attacks_detected": total_attacks_detected,
            "total_attacks_blocked": total_attacks_blocked
        }
        os.makedirs(os.path.dirname(STATE_DB_PATH), exist_ok=True)
        with open(STATE_DB_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"[-] DATABASE ERROR: Gagal menyimpan state -> {e}")
