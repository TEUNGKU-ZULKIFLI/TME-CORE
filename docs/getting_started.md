<h1 align="center">
  <img src="https://img.shields.io/badge/🚀_Getting_Started_with-TME--CORE-blue?style=for-the-badge" />
</h1>

Dokumen ini memandu Anda melakukan konfigurasi awal, memverifikasi kesehatan program menggunakan modul diagnosa internal, serta menjalankan TME-CORE sebagai layanan latar belakang secara terus-menerus.

## ⚙️ Langkah 1: Konfigurasi Variabel Lingkungan (.env)
TME-CORE memisahkan parameter kredensial sensitif dari logika program utama. Buka dan edit berkas `.env` yang berada di direktori *root* proyek Anda:
```bash
nano .env
```

Sesuaikan nilai variabel di dalamnya dengan topologi laboratorium Anda:
```env
# Alamat IP dan Kredensial Akses API Router MikroTik Anda
MIKROTIK_IP=192.168.10.1
MIKROTIK_PORT=8728
MIKROTIK_USER=admin
MIKROTIK_PASS=admin

# Whitelist IP Administrator (IP ini kebal dari pemblokiran & Zero Trust Kick)
WHITELIST_IPS=127.0.0.1,192.168.10.2

# Kredensial Notifikasi Telegram Bot API
TELEGRAM_TOKEN=1234567890:AAH_qWkLx2E8v9Yp...
TELEGRAM_CHAT_ID=987654321
```

> **Mendapatkan Kredensial `TOKEN` dan `CHAT ID` Telegram**
> - **Tahap 1: Membuat Bot (Token)**
>   1. Buka aplikasi Telegram Anda, cari akun resmi **`@BotFather`**, dan mulai percakapan (`/start`).
>   2. Kirim perintah `/newbot` untuk membuat bot baru.
>   3. Tentukan *Display Name* (contoh: `TME Security Guard`) dan *Username* (contoh: `tme_sec_bot`).
>   4. Setelah berhasil, `@BotFather` akan memberikan HTTP API Token. Salin token tersebut dan masukkan ke variabel `TELEGRAM_TOKEN`.
>
> - **Tahap 2: Mendapatkan Chat ID Pribadi**
>   1. Cari bot **`@userinfobot`** pada kolom pencarian Telegram, lalu kirim perintah `/start`.
>   2. Bot akan langsung merespons dengan detail profil Anda.
>   3. Salin deretan angka pada baris `Id:` dan masukkan ke variabel `TELEGRAM_CHAT_ID`.

<h3>Config Cast</h3>
<div id="config" class="cast-player"></div>

## 🔍 Langkah 2: Verifikasi Menggunakan TME-CORE Doctor
Sebelum menjalankan mesin pemantauan utama, jalankan modul diagnosa internal (*Pre-flight Doctor Check*) untuk memastikan server Debian dan router MikroTik siap berkolaborasi secara sempurna:
  - Aktifkan *virtual environment* Python:
  ```bash
  source venv/bin/activate
  ```

  - Jalankan *Doctor Check* dari modul utama:
  ```bash
  python3 -m src.main_engine
  ```
Sistem akan memvalidasi komponen dan memunculkan verifikasi visual kesehatan lingkungan kerja seperti di bawah ini:
```text
🔍 Menjalankan TME-CORE Doctor...
  [✓] Python Version : 3.11 (Terdukung)
  [✓] Environment    : File .env ditemukan
  [✓] Data Directory : Folder penyimpanan log siap
  [✓] Notifikasi     : Bot Telegram Terkonfigurasi
-----------------------------------------------------------------
[✓] Doctor: Semua sistem dalam kondisi PRIMA!
```

<h3>Main Engine Cast</h3>
<div id="main_engine" class="cast-player"></div>

## ⚙️ Langkah 3: Deployment (Menjalankan Sistem)
### Skenario A: Menjalankan Secara Manual (Fase Debugging)
Untuk memantau aktivitas sistem, penangkapan log, mitigasi, dan intervensi sesi (Jalur B) secara *real-time*, jalankan program penggerak utama pada terminal Anda:
```bash
python3 -m src.main_engine
```

> **Info:** TME-CORE terbaru dilengkapi dengan fitur *Quiet Mode* pada konektivitas API. *Engine* tidak akan melakukan *spam* pesan status koneksi, sehingga terminal Anda akan bersih dan hanya menampilkan penangkapan ancaman nyata (*Threat Detection*). Biarkan terminal tetap terbuka jika Anda sedang melakukan pengujian serangan *brute force*.

### Skenario B: Menjalankan Sebagai Layanan Latar Belakang (Systemd)
Untuk menjamin TME-CORE tetap mengamankan jaringan produksi Anda selama 24 jam tanpa henti, konfigurasikan program sebagai *Linux System Service*:
  1. Salin berkas unit layanan ke direktori systemd Linux:
  ```bash
  sudo cp assets/tmecore.service /etc/systemd/system/
  ```

  2. *Reload* daemon sistem, aktifkan *auto-start* saat *booting*, dan mulai eksekusi layanan:
  ```bash
  sudo systemctl daemon-reload
  sudo systemctl enable tmecore.service
  sudo systemctl start tmecore.service
  ```

  3. Verifikasi status operasional layanan:
  ```bash
  sudo systemctl status tmecore.service
  ```

  4. Lakukan pemantauan (*live tracking*) log internal *engine* melalui jurnal Linux:
  ```bash
  sudo journalctl -u tmecore.service -f
  ```

<h3>Systemd Daemon Cast</h3>
<div id="systemd_daemon" class="cast-player"></div>
