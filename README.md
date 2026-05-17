# 🚀 TME-CORE: MikroTik Threat Mitigation Engine

> **Deskripsi Singkat**  
TME-CORE adalah sistem otomatis untuk mitigasi serangan Brute Force SSH/FTP pada Router MikroTik.  
Engine berbasis Python ini berjalan di server Debian, menganalisa log secara real-time, mendeteksi anomali, dan melakukan blocking otomatis via API RouterOS dengan latency < 5 detik. ⚡

---

## 📚 Tahapan Setup
1. 🛠️ [TAHAP 1: Jembatan komunikasi ke RouterOS](docs/tahap1.md)  
2. 📡 [TAHAP 2: Pengecekan Raw Data Log MikroTik](docs/tahap2.md)
3. 🕵️‍♂️ [TAHAP 3: Jalur A - Mendeteksi log Brute Force](docs/tahap3.md)
4. 👁️ [TAHAP 4: Jalur B - Menganalisa Beban Router (CPU Monitor)](docs/tahap4.md)
5. ⚙️ [TAHAP 5: Menggabungkan Jalur A (Deteksi) & Jalur B (Evaluasi Kinerja)](docs/tahap5.md)
6. 📩 [TAHAP 6: Mengirim Notifikasi ke Telegram](docs/tahap6.md)

---

## ✨ Fitur Utama
- 🔍 Analisis log real-time
- 🛡️ Deteksi anomali brute force
- ⚡ Blocking otomatis < 5 detik
- 🔗 Integrasi langsung dengan RouterOS API

---

## 🎯 Tujuan
Memberikan perlindungan ekstra pada Router MikroTik dengan cara yang **ringan, cepat, dan fun** untuk sysadmin yang ingin tidur lebih nyenyak 😴.
