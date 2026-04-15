# TME-CORE (Traffic Mitigation External Core)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)

**TME-CORE** adalah sistem mitigasi otonom berbasis Python yang dirancang untuk melindungi infrastruktur MikroTik dari serangan *Brute Force* masif pada layanan SSH (Port 22) dan FTP (Port 21). Sistem ini menerapkan strategi **offloading processing**, di mana beban analisis log yang berat dipindahkan dari CPU router ke *External Engine* (Debian) untuk mencegah terjadinya *CPU exhaustion* atau kelumpuhan perangkat utama.

---

## ✨ Fitur Utama (Dual-Path Detection)

Sistem ini mengadopsi mekanisme deteksi hibrida untuk responsibilitas keamanan maksimal:

1.  **Jalur A (Brute Force Detection):** Memantau kegagalan login masif ($\ge 10$ kali dalam interval 1 menit) dan mengeksekusi pemblokiran otomatis pada *firewall*.
2.  **Jalur B (Anomaly Detection):** Mendeteksi alamat IP yang berhasil autentikasi (*Login Success*) namun memicu lonjakan beban CPU secara anomali pasca-autentikasi.
3.  **Autonomous Mitigation:** Penambahan alamat IP penyerang ke dalam *firewall address-list* dengan aksi *drop* secara dinamis melalui API port 8728.
4.  **Real-time Alerting:** Laporan insiden instan dikirim ke administrator melalui Bot Telegram dengan target latensi di bawah 7 detik.

---

## 🛠️ Arsitektur & Teknologi

Sistem dirancang dengan spesifikasi teknis sebagai berikut:
*   **Engine:** Python 3.12+ (Direkomendasikan karena Python 3.8 sudah mencapai status EOL/End of Life).
*   **Komunikasi:** MikroTik API (Port 8728) menggunakan pustaka `routeros-api`.
*   **Notifikasi:** Telegram Bot API.
*   **Target OS:** MikroTik RouterOS v6.43+ (Mendukung CHR maupun Hardware fisik seperti RB750Gr3).

---

## 📈 Metrik Evaluasi (NDLC)

Penelitian ini menggunakan kerangka kerja **Network Development Life Cycle (NDLC)** dengan fokus pada metrik performa berikut:
*   **Mean Time to Respond (MTTR):** Target mitigasi otonom di bawah 5 detik (Reduksi > 60% dibanding respon manual).
*   **CPU Utilization:** Efisiensi beban kerja prosesor melalui strategi *offloading*.
*   **Attack Detection Rate (ADR):** Akurasi deteksi serangan ditargetkan mencapai 100%.
*   **Network Stability:** Menjaga stabilitas *latency* dan *packet loss* bagi pengguna sah selama fase mitigasi berlangsung.

---

## 🚀 Cara Memulai

### 1. Prasyarat (Prerequisites)
*   Router MikroTik dengan layanan API aktif: `/ip service set api port=8728 disabled=no`.
*   Server/PC dengan OS Debian 11 sebagai pengontrol eksternal.

### 2. Instalasi
```bash
# Clone repository
git clone https://github.com/TEUNGKU-ZULKIFLI/TME-CORE.git
cd TME-CORE

# Install dependencies
pip install -r requirements.txt
```

### 3. Konfigurasi
Salin file `.env.example` menjadi `.env` dan lengkapi kredensial Anda:
```env
MT_HOST=192.168.88.1
MT_USER=admin
MT_PASS=password_anda
TELE_TOKEN=token_bot_telegram
CHAT_ID=id_chat_anda
```

### 4. Menjalankan Sistem
```bash
python main.py
```

---

**License:** [MIT License](LICENSE)