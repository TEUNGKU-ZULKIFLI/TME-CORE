# ==========================================
# FILE: src/alert/notifier.py
# FUNGSI: Mengirim Notifikasi ke Telegram dengan Template Terpadu
# ==========================================
import requests
import datetime
import os
from typing import Dict, Any, Optional

class TelegramNotifier:
    def __init__(self, token: str, chat_id: str):
        self.token = token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{self.token}/sendMessage"

    def format_threat_alert(self, threat_data: Dict[str, Any], cpu: Optional[int] = None,
                          ram_mb: Optional[float] = None, failed_count: Optional[int] = None) -> str:
        ip = threat_data.get('ip', 'N/A')
        threat_type = threat_data.get('threat_type', 'UNKNOWN')
        severity = threat_data.get('severity', 'MEDIUM')
        service = threat_data.get('service', 'N/A')
        username = threat_data.get('username', 'N/A')

        # Map threat type ke emoji
        threat_emoji = {
            'BRUTE_FORCE': '🔓',
            'UNAUTHORIZED_SUCCESS': '🚨',
            'BYPASS_BLOCKED': '🔥'
        }.get(threat_type, '⚠️')

        # Status action
        action_status = "BLOCKED & BLACKLISTED"
        if threat_type == 'UNAUTHORIZED_SUCCESS':
            action_status = "BLOCKED & SESSION KICKED"
        elif threat_type == 'BYPASS_BLOCKED':
            action_status = "SECONDARY BLOCK (Anomaly Detected)"

        # Severity emoji
        sev_emoji = {'CRITICAL': '🔴', 'HIGH': '🟠', 'MEDIUM': '🟡'}.get(severity, '⚪')

        # Build message
        msg = (
            f"{threat_emoji} *TME-CORE SECURITY ALERT* {sev_emoji}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"\n"
            f"*Threat Type:* `{threat_type}`\n"
            f"*Severity:* {sev_emoji} {severity}\n"
            f"*Attacker IP:* `{ip}`\n"
            f"*Service:* `{service}`\n"
            f"*Target User:* `{username}`\n"
        )

        if failed_count is not None and failed_count > 0:
            msg += f"*Failed Attempts:* {failed_count}x dalam batas waktu\n"

        msg += f"*Action:* {action_status}\n"

        if cpu is not None or ram_mb is not None:
            msg += f"\n*System Load (saat mitigasi):*\n"
            if cpu is not None:
                cpu_status = "🔴 CRITICAL" if cpu >= 80 else "🟡 WARNING" if cpu >= 50 else "🟢 NORMAL"
                msg += f"  • CPU: {cpu}% {cpu_status}\n"
            if ram_mb is not None:
                msg += f"  • Free RAM: {ram_mb:.1f} MB\n"

        msg += f"\n━━━━━━━━━━━━━━━━━━━━━━━━\n"
        msg += f"🕐 {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        msg += f"🛡️ _TME-CORE Autonomous Mitigation Engine_"

        return msg

    def send_alert(self, threat_data: Dict[str, Any], cpu: Optional[int] = None,
                  ram_mb: Optional[float] = None, failed_count: Optional[int] = None) -> bool:

        if not self.token or not self.chat_id:
            print("[-] Telegram Token atau Chat ID belum dikonfigurasi.")
            return False

        message = self.format_threat_alert(threat_data, cpu=cpu, ram_mb=ram_mb, failed_count=failed_count)

        try:
            payload = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': 'Markdown'
            }
            response = requests.post(self.api_url, json=payload, timeout=5)
            if response.status_code == 200:
                print(f"[✓] Notifikasi Telegram berhasil dikirim!")
                return True
            else:
                print(f"[✗] Gagal mengirim Telegram ({response.status_code}): {response.text}")
                return False
        except Exception as e:
            print(f"[✗] Error saat koneksi ke API Telegram: {e}")
            return False

    def send_raw_message(self, text: str, parse_mode: str = 'Markdown') -> bool:
        if not self.token or not self.chat_id:
            print("[-] Telegram Token atau Chat ID belum dikonfigurasi.")
            return False
        try:
            payload = {'chat_id': self.chat_id, 'text': text, 'parse_mode': parse_mode}
            response = requests.post(self.api_url, json=payload, timeout=5)
            if response.status_code == 200:
                print(f"[✓] Pesan Telegram (raw) berhasil dikirim")
                return True
            else:
                print(f"[✗] Gagal mengirim Telegram (raw) ({response.status_code}): {response.text}")
                return False
        except Exception as e:
            print(f"[✗] Error koneksi Telegram (raw): {e}")
            return False


# --- Blok Testing Mandiri ---
if __name__ == "__main__":
    print("=== TESTING MODUL TELEGRAM NOTIFIER ===")
    dummy_threat = {
        'ip': '203.0.113.42',
        'threat_type': 'UNAUTHORIZED_SUCCESS',
        'severity': 'CRITICAL',
        'service': 'winbox',
        'username': 'admin'
    }
    
    # Kita hanya mencetak template untuk mengecek kerapian format
    tester = TelegramNotifier("DUMMY_TOKEN", "DUMMY_CHAT_ID")
    formatted_msg = tester.format_threat_alert(dummy_threat, cpu=45, ram_mb=128.5, failed_count=1)
    
    print("\n[Preview Pesan Telegram]:\n")
    print(formatted_msg)
    print("\n[!] Pesan tidak dikirim karena menggunakan DUMMY_TOKEN.")
