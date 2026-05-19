<p align="center">
    <picture>
      <source media="(prefers-color-scheme: light)" srcset="./assets/logos/TME-banner.png" />
      <img src="./assets/logos/TME-banner.png" />
  </picture>
</p>
<h1 align="center">
  <span>TME-CORE</span>
  <br align="center">Teungku Mitigation Engine - Core</br>
</h1>
<p align="center">
<span align="center">TME-CORE adalah sistem otomatis untuk mitigasi serangan Brute Force SSH/FTP pada Router MikroTik. Engine berbasis Python ini berjalan di server Debian, menganalisa log secara real-time, mendeteksi anomali, dan melakukan blocking otomatis via API RouterOS dengan latency < 5 detik. ⚡</span>
</p>

## 🕐 History Tahapan Setup
1. 🛠️ [TAHAP 1: Jembatan komunikasi ke RouterOS](docs/tahap1.md)
2. 📡 [TAHAP 2: Pengecekan Raw Data Log MikroTik](docs/tahap2.md)
3. 🕵️‍♂️ [TAHAP 3: Jalur A - Mendeteksi log Brute Force](docs/tahap3.md)
4. 👁️ [TAHAP 4: Jalur B - Menganalisa Beban Router (CPU Monitor)](docs/tahap4.md)
5. ⚙️ [TAHAP 5: Menggabungkan Jalur A (Deteksi) & Jalur B (Evaluasi Kinerja)](docs/tahap5.md)
6. 📩 [TAHAP 6: Mengirim Notifikasi ke Telegram](docs/tahap6.md)
7. 🕐 [TAHAP 7: Menjadikan TME-CORE Berjalan di Background (Systemd)](docs/tahap7.md)
