# =========================================================
# FILE: src/db/state_manager.py
# FUNGSI: Ingatan Permanen (State Persistence) TME-CORE
# =========================================================
import json
import os
import datetime
from config.config import STATE_DB_PATH, MAX_FAILED_ATTEMPTS, STATE_RETENTION_SECONDS

def load_state():
    if not os.path.exists(STATE_DB_PATH):
        print(f"[*] Database: File belum ada ({STATE_DB_PATH}). Memulai dengan state kosong.")
        return {}, set(), {}, 0, 0

    try:
        with open(STATE_DB_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)

        raw_failed = data.get("failed_attempts", {})

        # Normalize failed_attempts values to list of timestamps (backwards-compatible)
        failed_attempts = {}
        for k, v in raw_failed.items():
            if isinstance(v, list):
                failed_attempts[k] = v
            elif isinstance(v, int):
                # legacy storage as counts -> convert to empty list (cannot reconstruct timestamps)
                failed_attempts[k] = []
            else:
                failed_attempts[k] = []

        blocked_ips_list = data.get("session_blocked_ips", [])
        session_blocked_ips = set(blocked_ips_list)

        # Persistent counts (carry-over between restarts)
        persistent_failed_counts = data.get("persistent_failed_counts", {})
        # normalize: ensure dict[ip] = {'count': int, 'last': float}
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

        # Tampilkan status restore secara jelas
        num_failed_ips = len(failed_attempts)
        num_blocked_ips = len(session_blocked_ips)

        print(f"\n[✓] DATABASE RESTORED:")
        print(f"    ├─ Failed IPs (Recent Attempts): {num_failed_ips}")
        if num_failed_ips > 0:
            for ip, hist in sorted(failed_attempts.items()):
                print(f"    │  └─ {ip}: {len(hist)} attempt(s) dalam time_window")
        print(f"    ├─ Blocked IPs (Firewall): {num_blocked_ips}")
        if num_blocked_ips > 0:
            for ip in sorted(session_blocked_ips):
                print(f"    │  └─ {ip}")

        # persistent counts info with threshold context
        if normalized_pfc:
            print(f"    ├─ Persistent Failure Counts (Threshold={MAX_FAILED_ATTEMPTS}, Retention={STATE_RETENTION_SECONDS}s): {len(normalized_pfc)}")
            for ip, entry in sorted(normalized_pfc.items()):
                cnt = entry['count']
                status = "⚠️ NEAR THRESHOLD" if cnt >= (MAX_FAILED_ATTEMPTS - 2) else "OK"
                print(f"    │  └─ {ip}: {cnt}/{MAX_FAILED_ATTEMPTS} {status}")

        print(f"    ├─ Total Detected Attacks: {total_attacks_detected}")
        print(f"    └─ Total Blocked Attacks: {total_attacks_blocked}\n")

        return failed_attempts, session_blocked_ips, normalized_pfc, total_attacks_detected, total_attacks_blocked

    except json.JSONDecodeError as e:
        print(f"[-] DATABASE ERROR: File JSON corrupt ({STATE_DB_PATH}) -> {e}")
        print(f"[!] Memulai dengan state kosong.\n")
        return {}, set(), {}, 0, 0
    except Exception as e:
        print(f"[-] DATABASE ERROR: Gagal membaca {STATE_DB_PATH} -> {e}")
        print(f"[!] Memulai dengan state kosong.\n")
        return {}, set(), {}, 0, 0


def save_state(failed_attempts, session_blocked_ips, persistent_failed_counts=None, total_attacks_detected=0, total_attacks_blocked=0):
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
