# ==========================================
# FILE: src/monitoring/evaluator_jalur_b.py
# FUNGSI: Jalur B - Analisa Beban Router (CPU/RAM)
# ==========================================
import os
import csv
import datetime
from config.config import METRICS_CSV_PATH

def init_metrics_csv():
    """
    Memastikan file CSV untuk pencatatan evaluasi kinerja telah dibuat dengan header.
    """
    os.makedirs(os.path.dirname(METRICS_CSV_PATH), exist_ok=True)
    if not os.path.exists(METRICS_CSV_PATH):
        try:
            with open(METRICS_CSV_PATH, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    "Timestamp",
                    "IP Penyerang",
                    "Aktivitas",
                    "Beban CPU (%)",
                    "Sisa RAM (MB)",
                    "Total RAM (MB)"
                ])
            print(f"[✓] METRICS: File CSV diinisialisasi di {METRICS_CSV_PATH}")
        except Exception as e:
            print(f"[✗] METRICS ERROR: Gagal membuat file CSV: {e}")


def record_performance_to_csv(api, attacker_ip: str, action_taken: str):
    """
    Mencatat penggunaan resource RouterOS saat mitigasi ke berkas CSV.
    """
    init_metrics_csv()

    try:
        resources = api.get_resource('/system/resource').get()
        if not resources:
            return None, None

        data = resources[0]
        cpu_load = int(data.get('cpu-load', 0))
        free_memory = int(data.get('free-memory', 0)) / (1024 * 1024) # MB
        total_memory = int(data.get('total-memory', 1)) / (1024 * 1024) # MB

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(METRICS_CSV_PATH, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                timestamp,
                attacker_ip,
                action_taken,
                cpu_load,
                f"{free_memory:.2f}",
                f"{total_memory:.2f}"
            ])

        print(f"[✓] METRICS RECORDED: {action_taken} | CPU: {cpu_load}% | Free RAM: {free_memory:.2f}MB")
        return cpu_load, free_memory

    except Exception as e:
        print(f"[✗] METRICS ERROR: Gagal mencatat beban router ke CSV: {e}")
        return None, None


# --- Blok Testing Mandiri ---
if __name__ == "__main__":
    print("=== TESTING MODUL EVALUATOR JALUR B ===")
    
    # Mocking API Resource
    class MockResource:
        def get(self):
            return [{'cpu-load': '35', 'free-memory': '268435456', 'total-memory': '536870912'}]
    class MockAPI:
        def get_resource(self, path): return MockResource()

    mock = MockAPI()
    cpu, ram = record_performance_to_csv(mock, "192.168.20.88", "BYPASS_BLOCKED_TEST")
    print(f"Hasil Ekstraksi -> CPU: {cpu}%, Free RAM: {ram} MB")
