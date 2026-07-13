<h1 align="center">
  <img src="https://img.shields.io/badge/🔧_TROUBLESHOOTING_with-TME--CORE-orange?style=for-the-bad" />
</h1>

Dokumen ini merangkum daftar masalah umum yang sering dihadapi oleh administrator jaringan saat mengintegrasikan TME-CORE dengan MikroTik beserta solusinya.

## 🚨 Masalah 1: Error Gagal Koneksi ke MikroTik API
<h3>Tampilan Log Terminal:</h3>

```
[-] GAGAL KONEKSI: Pastikan API MikroTik aktif (/ip services enable api)
[-] Error Log: [Errno 111] Connection refused
```

<h3>Penyebab:</h3>

1. Layanan API MikroTik pada port default `8728` belum diaktifkan di sisi RouterOS.
2. Alamat IP server Debian terhalang oleh aturan firewall filter MikroTik atau tidak berada dalam parameter `address` yang diizinkan pada konfigurasi layanan API router.

<h3>Solusi:</h3>

1. Masuk ke Winbox, buka menu **IP > Services**, pastikan service **api** aktif (tanda centang hijau) dan port bernilai `8728`.
2. Jika Anda menerapkan pembatasan IP akses pada API, hapus atau sesuaikan IP tersebut agar mencakup alamat IP server Debian Anda:

```
/ip service set api address=0.0.0.0/0
```

## 🚨 Masalah 2: ModuleNotFoundError saat Menjalankan Main Engine
<h3>Tampilan Log Terminal:</h3>

```
ModuleNotFoundError: No module named 'routeros_api'
```

<h3>Penyebab:</h3>

Anda menjalankan modul Python utama di luar lingkungan *Virtual Environment* (`venv`) yang berisi seluruh pustaka dependensi terpasang.

<h3>Solusi:</h3>

Aktifkan kembali lingkungan virtual Python sebelum menjalankan program:

```
source venv/bin/activate
python3 -m src.main_engine
```

## 🚨 Masalah 3: Masalah Izin Eksekusi Skrip (Permission Denied)
<h3>Tampilan Log Terminal:</h3>

```
bash: ./install.sh: Permission denied
```

<h3>Penyebab:</h3>

Berkas skrip otomatisasi `install.sh` kehilangan hak izin eksekusi (*execute permission*) pada sistem operasi Linux Debian.

<h3>Solusi:</h3>

Berikan hak izin eksekusi menggunakan utilitas `chmod`, lalu jalankan kembali skrip menggunakan perintah `source`:

```
chmod +x install.sh
source install.sh
```

## 🚨 Masalah 4: Kegagalan Pengiriman Notifikasi Telegram
<h3>Tampilan Log Terminal:</h3>

```
[-] GAGAL NOTIFIKASI: Telegram API Return -> {"ok":false,"error_code":401,"description":"Unauthorized"}
```

<h3>Penyebab:</h3>

Token bot Telegram (`TELEGRAM_TOKEN`) yang dikonfigurasi pada file `.env` salah, telah kedaluwarsa, atau tidak valid.

<h3>Solusi:</h3>

- Buka Telegram, hubungi `@BotFather` untuk memverifikasi ulang keaslian Token API Bot Anda.
- Periksa juga apakah *Chat ID* tujuan Anda sudah benar dan pastikan server Debian Anda memiliki jalur internet aktif (uji menggunakan `ping google.com`).
