# TME-CORE (Traffic Mitigation External Core)

**TME-CORE** adalah sistem mitigasi otomatis berbasis Python yang dirancang untuk melindungi router MikroTik dari serangan *Brute Force* pada layanan SSH (Port 22) dan FTP (Port 21). Sistem ini bekerja sebagai *External Engine* untuk menjaga stabilitas CPU router melalui strategi *offloading processing*.

---

## ✨ Fitur Utama (Logika Deteksi Ganda)

Sistem ini mengadopsi mekanisme deteksi dua jalur untuk responsibilitas keamanan maksimal:
- **Jalur A (Brute Force Detection):** Memantau kegagalan login masif ($\ge 10$ kali dalam 1 menit) dan melakukan pemblokiran otomatis pada *firewall*.
- **Jalur B (Cerdas/Anomali):** Mendeteksi alamat IP yang berhasil login (*Login Success*) namun memicu lonjakan beban CPU secara anomali.

---

## 🛠️ Arsitektur Teknologi

Sistem dibangun dengan spesifikasi teknis berikut:
- **Language:** Python 3.8+
- **Interface:** MikroTik API (Port 8728) menggunakan library `routeros-api`.
- **Notification:** Telegram Bot API untuk pelaporan *real-time*.
- **Target OS:** MikroTik RouterOS v6.43+ (CHR atau Hardware).

---

## 📈 Metrik Evaluasi (NDLC)

Penelitian ini mengukur kinerja sistem berdasarkan standar **Technology Rekayasa Komputer Jaringan (TRKJ)**:
1. **Mean Time to Respond (MTTR):** Target mitigasi < 5 detik.
2. **CPU Utilization:** Efisiensi beban kerja prosesor router.
3. **Attack Detection Rate (ADR):** Akurasi deteksi serangan hingga 100%.
4. **Network Stability:** Menjaga *latency* dan *packet loss* tetap stabil bagi pengguna sah.

---

## 🚀 Cara Memulai

*(Bagian ini akan diperbarui seiring berjalannya fase Implementation)*

1. Clone repository ini.
2. Siapkan file `.env` berisi kredensial MikroTik dan Token Telegram.
3. Jalankan `python3 main.py`.

---
**License:** [MIT License](LICENSE)
