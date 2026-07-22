# =================================================================
# FILE: src/monitoring/baseline_collector.py
# FUNGSI: Perekam Metrik Komprehensif (CPU, RAM, Latency, Packet Loss)
#         Untuk Pengambilan Data Baseline Bab 4 Skripsi
# =================================================================
import os
import sys
import time
import csv
import re
import subprocess
import datetime

# Setup Path Absolut agar bisa berjalan mandiri
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from config import config
from src.api.connection import connect_to_mikrotik, disconnect_from_mikrotik
from src.cli.console import print_banner

# Kelas warna ANSI untuk mempercantik output CLI
class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def ping_test(ip_target, count=5):
    try:
        # Menjalankan perintah ping di Linux Debian
        # ping -c 5 -W 1 <ip> -> kirim 5 paket, timeout 1 detik
        cmd = ["ping", "-c", str(count), "-W", "1", ip_target]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=7)
        output = result.stdout
        if not output:
            return 999.0, 100.0  # Latency tinggi, Loss 100% jika rute putus
        # 1. Ekstraksi Packet Loss (%) menggunakan Regex
        # Contoh output Linux: "5 packets transmitted, 5 received, 0% packet loss, time 4004ms"
        loss_match = re.search(r'(\d+)%\s+packet\s+loss', output)
        packet_loss = float(loss_match.group(1)) if loss_match else 0.0
        # 2. Ekstraksi Latency (Average RTT dalam ms)
        # Contoh output Linux: "rtt min/avg/max/mdev = 1.121/1.520/2.299/0.463 ms"
        rtt_match = re.search(r'rtt\s+min/avg/max/mdev\s+=\s+([\d\.]+)/([\d\.]+)/([\d\.]+)/([\d\.]+)', output)
        avg_latency = float(rtt_match.group(2)) if rtt_match else 0.0
        # Jika loss 100%, set Latency ke nilai penanda (misal 0 atau 999)
        if packet_loss == 100.0:
            avg_latency = 999.0
        return avg_latency, packet_loss
    except subprocess.TimeoutExpired:
        return 999.0, 100.0
    except Exception as e:
        # Fallback jika terjadi error internal sistem
        return 0.0, 0.0

def record_data_to_csv(filepath, record_no, cpu_load, ram_usage, latency, loss):
    # Memastikan folder direktori CSV ada
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    file_exists = os.path.exists(filepath)
    try:
        with open(filepath, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # Tulis header jika file baru dibuat
            if not file_exists:
                writer.writerow(["No", "Timestamp", "CPU (%)", "RAM (%)", "Latency (ms)", "Packet Loss (%)"])
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([record_no, timestamp, cpu_load, ram_usage, f"{latency:.3f}", f"{loss:.1f}"])
    except Exception as e:
        print(f"{Colors.RED}[-] Gagal menulis data ke CSV: {e}{Colors.RESET}")

def select_test_scenario():
    print_banner()
    print(f"{Colors.CYAN}🎯 MONITORING & DATA COLLECTOR BAB IV - TME-CORE{Colors.RESET}")
    print("=" * 65)
    print("Silakan pilih skenario pengambilan data penelitian Anda:")
    print(f" [{Colors.GREEN}1{Colors.RESET}] Pengambilan Data Kondisi Normal  -> (data_normal.csv)")
    print(f" [{Colors.GREEN}2{Colors.RESET}] Simulasi Serangan & Pencatatan  -> (data_serangan.csv)")
    print(f" [{Colors.GREEN}3{Colors.RESET}] Pengujian Repetisi Sistem       -> (data_repetisi.csv)")
    print("-----------------------------------------------------------------")
    while True:
        pilihan = input("Masukkan nomor pilihan (1/2/3): ").strip()
        if pilihan == '1':
            return os.path.join(config.DATA_DIR, "metrics", "data_normal.csv"), "KONDISI NORMAL"
        elif pilihan == '2':
            return os.path.join(config.DATA_DIR, "metrics", "data_serangan.csv"), "SIMULASI SERANGAN"
        elif pilihan == '3':
            return os.path.join(config.DATA_DIR, "metrics", "data_repetisi.csv"), "REPETISI SISTEM"
        else:
            print(f"{Colors.RED}[!] Input tidak valid. Masukkan angka 1, 2, atau 3.{Colors.RESET}")

def main():
    csv_file, skenario_name = select_test_scenario()
    print(f"\n{Colors.YELLOW}[*] Menghubungkan ke RouterOS MikroTik API...{Colors.RESET}")
    api_conn, pool = connect_to_mikrotik()
    if not api_conn:
        print(f"{Colors.RED}[-] Koneksi gagal. Mohon periksa kembali status router.{Colors.RESET}")
        return

    print(f"{Colors.GREEN}[✓] SUKSES: Terhubung ke {config.MIKROTIK_IP}{Colors.RESET}")
    print(f"[🛡️] Skenario Aktif: {Colors.BOLD}{skenario_name}{Colors.RESET}")
    print(f"[📂] File Output   : {Colors.CYAN}{csv_file}{Colors.RESET}")
    print("=" * 65)
    print(f"Memulai pemantauan. Tekan {Colors.RED}Ctrl+C{Colors.RESET} untuk menghentikan rekaman.")
    print("-" * 65)
    record_no = 1
    try:
        while True:
            # 1. Fetch data CPU dan RAM dari MikroTik API
            try:
                resources = api_conn.get_resource('/system/resource').get()
                if resources:
                    resource_data = resources[0]
                    cpu_load = int(resource_data.get('cpu-load', 0))
                    free_mem = int(resource_data.get('free-memory', 0))
                    total_mem = int(resource_data.get('total-memory', 1))
                    used_mem = total_mem - free_mem
                    ram_percent = int((used_mem / total_mem) * 100)
                else:
                    cpu_load, ram_percent = 0, 0
            except Exception as e:
                print(f"{Colors.RED}[-] API Gagal mengambil resource: {e}{Colors.RESET}")
                cpu_load, ram_percent = 0, 0
            # 2. Ambil data Latency & Loss via Ping dari Debian ke MikroTik
            latency, loss = ping_test(config.MIKROTIK_IP, count=5)
            # 3. Tampilkan secara real-time di CLI
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] #{record_no:03d} | "
                  f"CPU: {cpu_load:3d}% | "
                  f"RAM: {ram_percent:2d}% | "
                  f"Latency: {latency:6.3f} ms | "
                  f"Loss: {loss:5.1f}%")
            # 4. Simpan data secara rapi ke file CSV tujuan
            record_data_to_csv(csv_file, record_no, cpu_load, ram_percent, latency, loss)
            record_no += 1
            time.sleep(3)  # Interval pengujian 3 detik sekali
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[*] Perekaman dihentikan oleh Administrator.{Colors.RESET}")
        print(f"{Colors.GREEN}[✓] Seluruh data berhasil diekspor dengan aman ke {csv_file}!{Colors.RESET}")
    finally:
        disconnect_from_mikrotik(pool)

if __name__ == "__main__":
    main()
