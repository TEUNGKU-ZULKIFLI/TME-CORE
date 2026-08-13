# ==========================================
# FILE: src/parser/log_parser.py
# FUNGSI: Pengecekan & Parsing Raw Data Log MikroTik
# ==========================================

import re
from typing import Dict, Any, Optional, List

def parse_single_log(log_item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Merapikan dan mengekstrak informasi penting dari 1 baris log MikroTik.
    """
    message = log_item.get('message', '')
    log_id = log_item.get('id', '')
    timestamp = log_item.get('time', '')

    # 1. Regex untuk Login SUKSES (SSH, FTP, API, Winbox, Web, dll.)
    # Contoh pesan: "user admin logged in from 192.168.20.3 via ssh"
    pattern_success = r"user\s+(?P<username>\S+)\s+logged in from\s+(?P<ip>\d{1,3}(?:\.\d{1,3}){3})\s+via\s+(?P<service>\S+)"
    match_success = re.search(pattern_success, message)

    if match_success:
        return {
            'log_id': log_id,
            'timestamp': timestamp,
            'username': match_success.group('username'),
            'ip': match_success.group('ip'),
            'service': match_success.group('service').lower(),
            'status': 'SUCCESS',
            'raw_message': message
        }

    # 2. Regex untuk Login GAGAL (Brute-Force attempt)
    # Contoh pesan: "login failure for user admin from 192.168.20.3 via ssh"
    pattern_failed = r"login failure for user\s+(?P<username>\S+)\s+from\s+(?P<ip>\d{1,3}(?:\.\d{1,3}){3})\s+via\s+(?P<service>\S+)"
    match_failed = re.search(pattern_failed, message)

    if match_failed:
        return {
            'log_id': log_id,
            'timestamp': timestamp,
            'username': match_failed.group('username'),
            'ip': match_failed.group('ip'),
            'service': match_failed.group('service').lower(),
            'status': 'FAILED',
            'raw_message': message
        }

    # Log lain di luar masalah autentikasi diabaikan
    return None


def fetch_and_parse_logs(api_connection) -> List[Dict[str, Any]]:
    """
    Mengambil daftar log dari MikroTik via API dan memparsing log yang relevan.
    """
    parsed_results = []
    try:
        raw_logs = api_connection.get_resource('/log').get()
        for log in raw_logs:
            parsed_data = parse_single_log(log)
            if parsed_data:
                parsed_results.append(parsed_data)
    except Exception as e:
        print(f"[✗] Error saat mengambil log dari API: {e}")

    return parsed_results


# --- Blok Testing Mandiri ---
if __name__ == "__main__":
    print("=== TESTING MODUL LOG PARSER ===")
    
    sample_logs = [
        {'id': '*1', 'time': '17:00:01', 'message': 'user admin logged in from 192.168.10.2 via api'},
        {'id': '*2', 'time': '17:00:05', 'message': 'login failure for user admin from 192.168.20.40 via ssh'},
        {'id': '*3', 'time': '17:00:10', 'message': 'user admin logged in from 192.168.20.40 via ssh'},
        {'id': '*4', 'time': '17:00:15', 'message': 'system,info router rebooted'},
    ]

    for raw in sample_logs:
        parsed = parse_single_log(raw)
        if parsed:
            print(f"[✓] PARSED [{parsed['status']}]: IP={parsed['ip']} | User={parsed['username']} | Service={parsed['service']}")
        else:
            print(f"[-] IGNORED: {raw['message']}")
