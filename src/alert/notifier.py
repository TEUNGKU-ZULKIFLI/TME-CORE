# ==========================================
# FILE: src/alert/notifier.py
# FUNGSI: Mengirim Notifikasi ke Telegram dengan Template Terpadu
# ==========================================
import requests
import datetime
from typing import Dict, Any, Optional

class TelegramNotifier:
    def __init__(self, token: str, chat_id: str):
        """Inisialisasi bot Telegram dengan Bot Token dan Chat ID."""
        self.token = token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{self.token}/sendMessage"

    def format_threat_alert(self, threat_data: Dict[str, Any], cpu: Optional[int] = None, 
                          ram_mb: Optional[float] = None, failed_count: Optional[int] = None) -> str:
        """
        Format pesan alert menggunakan template terpadu.
        
        Params:
        - threat_data: dict dengan keys: threat_type, ip, service, username, severity, message (opsional)
        - cpu: persentase CPU saat mitigasi
        - ram_mb: RAM bebas dalam MB
        - failed_count: jumlah percobaan gagal sebelumnya
        
        Returns: formatted message (Markdown)
        """
        ip = threat_data.get('ip', 'N/A')
        threat_type = threat_data.get('threat_type', 'UNKNOWN')
        severity = threat_data.get('severity', 'MEDIUM')
        service = threat_data.get('service', 'N/A')
        username = threat_data.get('username', 'N/A')
        
        # Map threat type ke emoji dan deskripsi
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
            msg += f"*Failed Attempts:* {failed_count}x dalam 60 detik\n"
        
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
        """
        Mengirim alert threat ke Telegram menggunakan template terpadu.
        
        Params:
        - threat_data: dict threat info
        - cpu: optional CPU %
        - ram_mb: optional RAM free
        - failed_count: optional jumlah percobaan gagal
        """
        if not self.token or not self.chat_id:
            print("[-] Telegram Token atau Chat ID belum dikonfigurasi di .env")
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
                print(f"[✓] Notifikasi Telegram berhasil dikirim")
                return True
            else:
                print(f"[✗] Gagal mengirim Telegram ({response.status_code}): {response.text}")
                return False
        except Exception as e:
            print(f"[✗] Error saat koneksi ke API Telegram: {e}")
            return False

    def send_raw_message(self, text: str, parse_mode: str = 'Markdown') -> bool:
        """Mengirim pesan custom langsung ke Telegram."""
        if not self.token or not self.chat_id:
            print("[-] Telegram Token atau Chat ID belum dikonfigurasi di .env")
            return False

        try:
            payload = {
                'chat_id': self.chat_id,
                'text': text,
                'parse_mode': parse_mode
            }
            response = requests.post(self.api_url, json=payload, timeout=5)
            if response.status_code == 200:
                print(f"[✓] Notifikasi Telegram (raw) berhasil dikirim")
                return True
            else:
                print(f"[✗] Gagal mengirim Telegram (raw) ({response.status_code}): {response.text}")
                return False
        except Exception as e:
            print(f"[✗] Error saat koneksi ke API Telegram (raw): {e}")
            return False


# Testing
if __name__ == "__main__":
    from config.config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
    print("=== TESTING NOTIFIER TEMPLATE ===")
    notifier = TelegramNotifier(token=TELEGRAM_TOKEN, chat_id=TELEGRAM_CHAT_ID)
    
    test_threat = {
        'threat_type': 'BRUTE_FORCE',
        'severity': 'HIGH',
        'ip': '192.168.20.5',
        'service': 'ssh',
        'username': 'root'
    }
    
    msg = notifier.format_threat_alert(test_threat, cpu=65, ram_mb=8.5, failed_count=5)
    print(msg)
    print("\n--- Mengirim (jika token ada) ---")
    notifier.send_alert(test_threat, cpu=65, ram_mb=8.5, failed_count=5)
