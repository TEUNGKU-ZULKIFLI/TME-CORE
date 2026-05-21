<p align="center">
  <picture>
    <source media="(prefers-color-scheme: night)" srcset="../assets/logos/TME-logo01.png" />
    <img src="../assets/logos/TME-logo01.png" width="500" />
  </picture>
</p>
<h1 align="center">
  <span><b align="center">🧑‍💻 TAHAP: Menjadikan TME-CORE Berjalan di Background (Systemd)</b></span>
</h1>

**Deskripsi**:</br>
Menyetup agar `Engine TME-CORE` ini berjalan 24 Jam.

> [!WARNING]
> > **`SUDAH MENGIKUTI TAHAPAN BERIKUT INI:`**</br>
> > **🧑‍💻 TAHAP: Jembatan komunikasi ke RouterOS**</br>
> > **Deskripsi**:</br>
> > *Membangun koneksi dasar!*</br>
> > **🧑‍💻 TAHAP: Pengecekan Raw Data Log MikroTik**</br>
> > **Deskripsi**:</br>
> > *Mengambil data log mikrotik dasar dengan 5 RAW LOG TERAKHIR!*</br>
> > *Pada Dasarnya sama seperti terminal mikrotik dengan `log print`*</br>
> > **🧑‍💻 TAHAP: Jalur A - Mendeteksi log Brute Force**</br>
> > **Deskripsi**:</br>
> > *Mendeteksi dengan cara memantau log berkala, serta membatasi jika kegagalan login mencapai `THRESHOLD` maka siap untuk dikirimkan ke`modul blokir`.*</br>
> > **🧑‍💻 TAHAP: Jalur B - Menganalisa Beban Router (CPU Monitor)**</br>
> > **Deskripsi**:</br>
> > *Memonitoring secara berkala **`CPU & Memory`** Router.*</br>
> > **🧑‍💻 TAHAP: Menggabungkan Jalur A (Deteksi) & Jalur B (Evaluasi Kinerja)**</br>
> > **Deskripsi**:</br>
> > *Membaca **`/log (Jalur A)`**. Hanya jika ada indikasi `Brute Force`, baru membaca **`/system/resource (Jalur B)`** untuk merekam beban CPU saat itu, mencatatnya ke **`file log`**.*</br>
> > **🧑‍💻 TAHAP: Mengirim Notifikasi ke Telegram**</br>
> > **Deskripsi**:</br>
> > *Menyetup sebuah Bot untuk memberitahukan bahwa IP penyerang sudah terblokir nih!*</br>

#### TAHAP 7: Panduan Menjadikan TME-CORE Berjalan di Background (Systemd)
Jalankan perintah-perintah ini di terminal Server kamu (sebagai `root` atau pakai `sudo`).</br>

1. Buat file service baru:
```bash
sudo nano /etc/systemd/system/tmecore.service
```
2. Copy dan Paste kode di bawah ini ke dalam nano:
> [!WARNING]
> **Pastikan jalurnya `/home/<username>/TME-CORE/` sudah benar sesuai tempat kamu cloning Repo ini**
```bash
[Unit]
Description=TME-CORE MikroTik Mitigation Engine
After=network.target

[Service]
# User yang menjalankan script
User=<username>
WorkingDirectory=/home/<username>/TME-CORE
# Path ke Python di dalam Virtual Environment kamu
ExecStart=/home/<username>/TME-CORE/venv/bin/python3 -m src.main_engine
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

> [!CAUTION]
> **Patikan path sesuai dengan server Anda `/home/<username>/TME-CORE/`**
> ```bash
> pwd
> ```

3. Simpan dan Keluar dari nano (`Ctrl+o`, `Enter`, `Ctrl+x`).

4. Aktifkan dan jalankan servicenya:
```bash
sudo systemctl daemon-reload
```
```bash
sudo systemctl enable tmecore.service
```
```bash
sudo systemctl start tmecore.service
```
5. Cara mengecek apakah TME-CORE berjalan:
```bash
sudo systemctl status tmecore.service
```
6. Cara melihat Log (Terminal Output) TME-CORE secara live:
```bash
sudo journalctl -u tmecore.service -f
```
<p align=right>
<a href="./tahap6.md#--%E2%80%8D-tahap-mengirim-notifikasi-ke-telegram">
  <img src="https://img.shields.io/badge/🔙-BACK-red?style=for-the-badge" />
</a>
<a href="./all-tahap.md#--teungku-mitigation-engine---core">
  <img src="https://img.shields.io/badge/🏁-MAIN-green?style=for-the-badge" />
</a>
</p>