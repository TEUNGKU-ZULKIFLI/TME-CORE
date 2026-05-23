<p align="center">
  <picture>
    <source media="(prefers-color-scheme: night)" srcset="../assets/logos/TME-logo01.png" />
    <img src="../assets/logos/TME-logo01.png" width="500" />
  </picture>
</p>
<h1 align="center">
  <span><b align="center">📥 INSTALLASI with TME-CORE</b></span>
</h1>

## Quick Guide
Clone pake **`SSH`**
```bash
git clone git@github.com:TEUNGKU-ZULKIFLI/TME-CORE.git
```
Atau memakai **`HTTPS`**
```bash
git clone https://github.com/TEUNGKU-ZULKIFLI/TME-CORE.git
```
Kemudian masuk kedirectory tersebut
```bash
cd TME-CORE
```
Running `install.sh` dengan `source`
```bash
chmod +x install.sh
```
```bash
source install.sh
```
Membuka dan Konfigurasi file **`.env`**
```bash
nano .env
```

> [!NOTE]
> Cara Mendapatkan **`TOKEN`** dan **`ID`** Bot Telegram
- **Pertama**:</br>
    - Pastikan sudah punya **`Account Telegram`** dong!</br>
    - Langsung ke `pencarian` dan ketik `@BotFather` dan pilih yang sesuai dengan yang tertera.
    - Gas **`START`**
- **Kedua**:</br>
    - Ketikkan pada kolom Pesan dengan `/newbot`
    - Berikan nama untuk bot contoh: `example`
    - Selanjutnya username bot contoh: `example_bot`
    - Jika berhasil nanti akan ditampilkan `Done! Conratulations on your new bot.`
    - Kemudian mencari kalimat `Use this token to access the HTTP API:` dan mencatat HTTP API nya. 
    - 🎉 Selamat kita sudah mendapatkan **`TOKEN`**
- **Ketiga**:</br>
    - Kembali ke `home` karena ada satu lagi yang kita perlukan!
    - Langsung ke `pencarian` dan ketik `@userinfobot` dan pilih yang sesuai dengan yang tertera.
    - Gas **`START`**
    - Setelah itu bot tersebut akan mengembalikan data-data seperti `@username_account` dan info lainnya.
    - Temukan `Id:xxxx` dan catat ke memo.
    - 🎉 Selamat kita sudah mendapatkan **`ID`**</br>

Setelah selesai menyesuaikan file Konfigurasi jalankan test koneksi
```bash
source venv/bin/activate && python3 -m src.api.connection
```

> [!IMPORTANT]
> Jika sudah berhasil terhubung maka bisa melanjutkan kedalam membuat service yang berjalan **`24 jam`**</br>
<a href="./getting_started.md#%EF%B8%8F-5-menjalankan-sebagai-layanan-247-systemd">
  <img src="https://img.shields.io/badge/⚙️-ENGINE-orange?style=for-the-badge" />
</a></br>