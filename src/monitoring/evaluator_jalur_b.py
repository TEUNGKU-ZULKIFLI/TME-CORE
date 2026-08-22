import os
import csv
import datetime
from config.config import METRICS_CSV_PATH

def init_metrics_csv():
    os.makedirs(os.path.dirname(METRICS_CSV_PATH), exist_ok=True)
    if not os.path.exists(METRICS_CSV_PATH):
        try:
            with open(METRICS_CSV_PATH, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    "Timestamp", "IP Penyerang", "Aktivitas", 
                    "Beban CPU (%)", "Sisa RAM (MB)", "Total RAM (MB)"
                ])
            print(f"[✓] METRICS: File CSV diinisialisasi di {METRICS_CSV_PATH}")
        except Exception as e:
            print(f"[✗] METRICS ERROR: Gagal membuat file CSV: {e}")

def record_performance_to_csv(api, attacker_ip: str, action_taken: str):
    init_metrics_csv()
    try:
        resources = api.get_resource('/system/resource').get()
        if not resources:
            return None, None

        data = resources[0]
        cpu_load = int(data.get('cpu-load', 0))
        free_memory = int(data.get('free-memory', 0)) / (1024 * 1024)
        total_memory = int(data.get('total-memory', 1)) / (1024 * 1024)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(METRICS_CSV_PATH, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                timestamp, attacker_ip, action_taken,
                cpu_load, f"{free_memory:.2f}", f"{total_memory:.2f}"
            ])

        print(f"[✓] METRICS RECORDED: {action_taken} | CPU: {cpu_load}% | Free RAM: {free_memory:.2f}MB")
        return cpu_load, free_memory
    except Exception as e:
        print(f"[✗] METRICS ERROR: Gagal mencatat beban router ke CSV: {e}")
        return None, None
