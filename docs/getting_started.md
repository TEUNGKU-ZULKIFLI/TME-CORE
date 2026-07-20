<h1 align="center">
  <img src="https://img.shields.io/badge/🚀_Getting_Started_with-TME--CORE-blue?style=for-the-bad" />
</h1>

Dokumen ini memandu Anda melakukan konfigurasi awal, memverifikasi kesehatan program menggunakan modul diagnosa internal, serta menjalankan TME-CORE sebagai layanan latar belakang secara terus-menerus.

## ⚙️ Langkah 1: Konfigurasi Variabel Lingkungan (.env)
TME-CORE memisahkan kredensial sensitif dari logika program utama. Buka dan edit berkas `.env` yang berada di direktori *root* proyek Anda:
```
nano .env
```

Sesuaikan nilai variabel di dalamnya dengan topology laboratorium Anda:
```
# Alamat IP dan Port API Router MikroTik Anda
MIKROTIK_IP=192.168.10.1
MIKROTIK_PORT=8728
MIKROTIK_USER=admin
MIKROTIK_PASS=admin

# Whitelist IP Administrator (IP ini kebal dari pemblokiran otomatis)
WHITELIST_IPS=127.0.0.1,192.168.10.2

# Kredensial Notifikasi Telegram Bot API
TELEGRAM_TOKEN=1234567890:AAH_qWkLx2E8v9Yp...
TELEGRAM_CHAT_ID=987654321
```

> Cara Mendapatkan **`TOKEN`** dan **`ID`** Bot Telegram
  - **Pertama**:</br>
      - Pastikan sudah punya **`Account Telegram`** dong!</br>
      - Langsung ke `pencarian` dan ketik `@BotFather` dan pilih yang sesuai dengan yang tertera.</br>
      - Gas **`START`**
  - **Kedua**:</br>
      - Ketikkan pada kolom Pesan dengan `/newbot`</br>
      - Berikan nama untuk bot contoh: `example`</br>
      - Selanjutnya username bot contoh: `example_bot`</br>
      - Jika berhasil nanti akan ditampilkan `Done! Conratulations on your new bot.`</br>
      - Kemudian mencari kalimat `Use this token to access the HTTP API:` dan mencatat HTTP API nya. </br>
      - 🎉 Selamat kita sudah mendapatkan **`TOKEN`**
  - **Ketiga**:</br>
      - Kembali ke `home` karena ada satu lagi yang kita perlukan!</br>
      - Langsung ke `pencarian` dan ketik `@userinfobot` dan pilih yang sesuai dengan yang tertera.</br>
      - Gas **`START`**</br>
      - Setelah itu bot tersebut akan mengembalikan data-data seperti `@username_account` dan info lainnya.</br>
      - Temukan `Id:xxxx` dan catat ke memo.</br>
      - 🎉 Selamat kita sudah mendapatkan **`ID`**</br>

<h3>Config Cast</h3>
<div id="config" class="cast-player"></div>

## 🔍 Langkah 2: Verifikasi Menggunakan TME-CORE Doctor
Sebelum menjalankan mesin pemantauan utama, jalankan modul diagnosa internal (*Pre-flight Doctor Check*) untuk memastikan server Debian dan router MikroTik siap berkolaborasi tanpa masalah:
  - Aktifkan virtual environment jika belum aktif
  ```
  source venv/bin/activate
  ```
  
  - Jalankan modul utama
  ```
  python3 -m src.main_engine
  ```
Sistem akan memunculkan verifikasi visual kesehatan lingkungan kerja seperti di bawah ini:
```
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
Untuk memantau aktivitas logs dan deteksi serangan secara real-time langsung pada terminal Anda, jalankan program utama:
```
python3 -m src.main_engine
```

Biarkan terminal tetap terbuka untuk memantau bagaimana *engine* mengekstrak IP penyerang menggunakan Regex saat uji coba serangan brute force dilakukan.

### Skenario B: Menjalankan Sebagai Layanan Latar Belakang (Systemd)
Untuk menjamin TME-CORE tetap mengamankan jaringan Anda selama 24 jam tanpa harus membiarkan terminal SSH Debian terbuka, pasang program sebagai *System Service*:
  1. Salin berkas unit layanan ke direktori systemd Linux:
  ```
  sudo cp assets/tmecore.service /etc/systemd/system/
  ```
  
  2. *Reload* daemon Linux, aktifkan fitur *auto-start* saat boot, dan jalankan layanan:
  ```
  sudo systemctl daemon-reload
  sudo systemctl enable tmecore.service
  sudo systemctl start tmecore.service
  ```
   
  3. Pantau status keaktifan layanan secara real-time:
  ```
  sudo systemctl status tmecore.service
  ```
  
  4. Lakukan live tracking log operasional melalui jurnal Linux:
  ```
  sudo journalctl -u tmecore.service -f
  ```

<h3>Systemd Daemon Cast</h3>
<div id="systemd_daemon" class="cast-player"></div>
