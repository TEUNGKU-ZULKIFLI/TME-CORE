# ========================================================
# FILE: src/cli/console.py
# FUNGSI: Mempercantik Terminal (Banner & Pre-flight Check)
# ========================================================
import os
import sys
import time

# Definisi Warna ANSI untuk Terminal Linux/Mac
class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def print_banner():
    """Mencetak ASCII Art yang elegan layaknya tools Hacking/DevOps"""
    os.system('clear' if os.name == 'posix' else 'cls') # Bersihkan layar

    banner = f"""{Colors.CYAN}{Colors.BOLD}
████████╗███╗   ███╗███████╗     ██████╗ ██████╗ ██████╗ ███████╗
╚══██╔══╝████╗ ████║██╔════╝    ██╔════╝██╔═══██╗██╔══██╗██╔════╝
   ██║   ██╔████╔██║█████╗█████╗██║     ██║   ██║██████╔╝█████╗
   ██║   ██║╚██╔╝██║██╔══╝╚════╝██║     ██║   ██║██╔══██╗██╔══╝
   ██║   ██║ ╚═╝ ██║███████╗    ╚██████╗╚██████╔╝██║  ██║███████╗
   ╚═╝   ╚═╝     ╚═╝╚══════╝     ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝
    {Colors.RESET}"""
    print(banner)
    print(f"{Colors.YELLOW} [🛡️] Teungku Mitigation Engine - Core (TME-CORE) v1.0.0{Colors.RESET}")
    print(f"{Colors.YELLOW} [🎓] Politeknik Negeri Lhokseumawe - Teknologi Rekayasa Komputer Jaringan{Colors.RESET}")
    print(f"{Colors.CYAN}{'=' * 65}{Colors.RESET}")

def run_doctor(env_path, data_dir, config_module):
    """
    Melakukan Pre-Flight Check
    sebelum Engine benar-benar berjalan.
    """
    print(f"\n{Colors.BOLD}🔍 Menjalankan TME-CORE Doctor...{Colors.RESET}")
    time.sleep(0.5)

    all_passed = True

    # 1. Cek Python Version
    py_version = sys.version_info
    if py_version.major >= 3 and py_version.minor >= 8:
        print(f"  [{Colors.GREEN}✓{Colors.RESET}] Python Version : {py_version.major}.{py_version.minor} (Terdukung)")
    else:
        print(f"  [{Colors.RED}✗{Colors.RESET}] Python Version : {py_version.major}.{py_version.minor} (Butuh >= 3.8)")
        all_passed = False

    # 2. Cek File .env
    if os.path.exists(env_path):
        print(f"  [{Colors.GREEN}✓{Colors.RESET}] Environment    : File .env ditemukan")
    else:
        print(f"  [{Colors.RED}✗{Colors.RESET}] Environment    : File .env HILANG! Gunakan nilai default.")
        all_passed = False

    # 3. Cek Folder Data
    if os.path.exists(data_dir):
        print(f"  [{Colors.GREEN}✓{Colors.RESET}] Data Directory : Folder penyimpanan log siap")
    else:
        print(f"  [{Colors.RED}✗{Colors.RESET}] Data Directory : Gagal membuat folder data/")
        all_passed = False

    # 4. Cek Telegram (Opsional)
    if config_module.TELEGRAM_TOKEN and config_module.TELEGRAM_CHAT_ID:
         print(f"  [{Colors.GREEN}✓{Colors.RESET}] Notifikasi     : Bot Telegram Terkonfigurasi")
    else:
         print(f"  [{Colors.YELLOW}!{Colors.RESET}] Notifikasi     : Telegram Token kosong (Berjalan Mode Senyap)")

    print(f"{Colors.CYAN}{'-' * 65}{Colors.RESET}")

    if not all_passed:
        print(f"{Colors.YELLOW}[!] Doctor mendeteksi beberapa isu, namun Engine akan tetap mencoba berjalan...{Colors.RESET}\n")
    else:
        print(f"{Colors.GREEN}[✓] Doctor: Semua sistem dalam kondisi PRIMA!{Colors.RESET}\n")

    time.sleep(1)
