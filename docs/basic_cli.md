<h1 align="center">
  <img src="https://img.shields.io/badge/⌨️_BASIC_CLI_with-TME--CORE-8A2BE2?style=for-the-badge" />
</h1>

Dokumen ini berisi daftar contekan (*cheat sheet*) perintah dasar untuk mengelola layanan TME-CORE dan menjalankan modul-modul pengujian internal.

## ⚙️ Manajemen Layanan (Systemd)
Pastikan Anda telah melakukan pengaturan Systemd sesuai panduan [Getting Started (Skenario B)](getting_started.md#skenario-b-menjalankan-sebagai-layanan-latar-belakang-systemd) sebelum menggunakan perintah di bawah ini.

### Memeriksa Status Mesin (Status)
Untuk melihat apakah layanan TME-CORE sedang berjalan dan melihat log terbaru:
```bash
sudo systemctl status tmecore.service
```

### Menghidupkan Mesin (Start)
Untuk memulai layanan pemantauan:
```bash
sudo systemctl start tmecore.service
```

### Menghentikan Mesin (Stop)
Untuk mematikan sementara layanan pemantauan:
```bash
sudo systemctl stop tmecore.service
```

### Memulai Ulang Mesin (Restart)
Sangat berguna jika Anda baru saja melakukan perubahan pada file `.env` atau pembaruan kode:
```bash
sudo systemctl restart tmecore.service
```

---

## 💻 Perintah Dasar CLI (Eksekusi Manual)
Gunakan perintah ini saat Anda sedang melakukan *debugging* atau pengetesan (*troubleshooting*) secara manual di terminal. 

> **⚠️ Penting:** Selalu pastikan Anda telah mengaktifkan lingkungan virtual sebelum menjalankan modul Python apa pun:
> ```bash
> source venv/bin/activate
> ```

### 🚀 Menjalankan Mesin Utama (Main Engine)
Menjalankan mesin deteksi, *parsing* log, dan mitigasi secara *real-time*:
```bash
python3 -m src.main_engine
```

### 📎 Uji Koneksi API (Test Connection)
Memverifikasi respons dan kredensial komunikasi port 8728 antara Debian dan MikroTik:
```bash
python3 -m src.api.connection
```

### 📃 Uji Ekstraksi Log (Test Log Parser)
Memvalidasi kemampuan *Regex* (Regular Expression) dalam membaca log ancaman dari memori *router*:
```bash
python3 -m src.parser.log_parser
```

### 👀 Pantauan Metrik (Test Monitoring Realtime)
Membaca beban CPU, memori RAM, dan parameter kesehatan *router* MikroTik secara langsung (menyimulasikan fungsi pengumpulan dataset skripsi):
```bash
python3 -m src.monitoring.realtime_cpu_ram
```
