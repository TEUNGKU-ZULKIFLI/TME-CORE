# =========================================================
# FILE: src/db/state_manager.py
# FUNGSI: Ingatan Permanen (State Persistence) TME-CORE
# =========================================================
import json
import os
from config import config

def load_state():
    if not os.path.exists(config.STATE_DB_PATH):
        # Jika belum ada database, kembalikan data default kosong
        return {}, set(), 0, 0
    try:
        with open(config.STATE_DB_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            failed_attempts = data.get("failed_attempts", {})
            blocked_ips_list = data.get("session_blocked_ips", [])
            session_blocked_ips = set(blocked_ips_list)
            total_attacks_detected = data.get("total_attacks_detected", 0)
            total_attacks_blocked = data.get("total_attacks_blocked", 0)
            print(f"[+] DATABASE: Berhasil memuat ingatan. ({len(session_blocked_ips)} IP Terblokir | Total Deteksi: {total_attacks_detected})")
            return failed_attempts, session_blocked_ips, total_attacks_detected, total_attacks_blocked
    except Exception as e:
        print(f"[-] DATABASE ERROR: Gagal membaca {config.STATE_DB_PATH} -> {e}")
        return {}, set(), 0, 0

def save_state(failed_attempts, session_blocked_ips, total_attacks_detected=0, total_attacks_blocked=0):
    try:
        data = {
            "failed_attempts": failed_attempts,
            "session_blocked_ips": list(session_blocked_ips),
            "total_attacks_detected": total_attacks_detected,
            "total_attacks_blocked": total_attacks_blocked
        }
        os.makedirs(os.path.dirname(config.STATE_DB_PATH), exist_ok=True)
        with open(config.STATE_DB_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        pass
