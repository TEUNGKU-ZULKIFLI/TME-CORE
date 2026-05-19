<p align="center">
    <picture>
      <source media="(prefers-color-scheme: light)" srcset="./assets/logos/TME-banner.png" />
      <img src="./assets/logos/TME-banner.png" />
  </picture>
</p>
<h1 align="center">
  <span>🚀 Getting Started with TME-CORE</span>
</h1>
<p align="center">
<span align="center">Selamat datang di panduan penggunaan <b>Teungku Mitigation Engine - Core (TME-CORE)</b>. Panduan ini akan memandu Anda langkah demi langkah untuk menghubungkan sistem deteksi ini dengan Router MikroTik Anda.</span>
</p>

## 📋 1. Persiapan Router MikroTik (Pre-requisites)

Sebelum menjalankan TME-CORE, Anda wajib melakukan sedikit konfigurasi di Router MikroTik target:</br>

1. **Aktifkan Layanan API**:</br>
Buka terminal MikroTik (New Terminal) atau SSH, lalu ketikkan:
```bash
/ip services enable api
```

2. **Buat Rule Firewall Block**:</br>
TME-CORE bertugas memasukkan IP penyerang ke dalam daftar hitam bernama `brute_force_block`. Anda harus membuat rule yang memblokir daftar tersebut:
```bash
/ip firewall filter add chain=input action=drop src-address-list=brute_force_block comment="Drop brute_force_block - TME-CORE"
```
> [!TIP]
> (Pastikan rule ini berada di urutan teratas/atas rule accept lainnya pada menu IP > Firewall > Filter Rules).

3. **(Opsional) Sinkronisasi Waktu**:</br>
Sangat disarankan mengaktifkan NTP Client di MikroTik agar log waktu akurat:
```bash
/system ntp client set enabled=yes primary-ntp=162.159.200.1
```

## 🛠️ 2. Konfigurasi Lingkungan (TME-CORE Server)

TME-CORE dapat diinstal di Linux Debian/Ubuntu (Server Lokal maupun Cloud VPS).</br>

**Langkah Instalasi Otomatis:**</br>

1. **Clone repositori ini**:</br>
**Menggunakan `SSH`**:
```bash
git clone git@github.com:TEUNGKU-ZULKIFLI/TME-CORE.git
```
**Atau dengan menggunakan `HTTP`**:
```bash
git clone https://github.com/TEUNGKU-ZULKIFLI/TME-CORE.git
```
**Kemudian masuk ke`Repo` tersebut dengan**:
```bash
cd TME-CORE
```

2. **Jalankan Script Installer**:
```bash
chmod +x install.sh
```
```bash
source install.sh
```

> [!IMPORTANT]
> *Script ini akan otomatis membuatkan Virtual Environment (**`venv`**) dan menginstal pustaka yang dibutuhkan*.

## 🔐 3. Mengisi Kredensial Rahasia (.env)

Keamanan adalah prioritas. TME-CORE menggunakan file `.env` untuk menyimpan kata sandi Anda.</br>

1. **Buka file `.env` menggunakan text editor (contoh: nano)**:
```bash
nano .env
```

2. **Sesuaikan isinya dengan topologi Anda**:
```config
# Ganti dengan IP dan Password MikroTik Anda
MIKROTIK_IP=192.168.10.1
MIKROTIK_USER=admin
MIKROTIK_PASS=password_rahasia
MIKROTIK_PORT=8728

# Masukkan IP Anda sendiri agar tidak keblokir saat salah password
WHITELIST_IPS=192.168.10.2,127.0.0.1

# Isi jika ingin menggunakan notifikasi Telegram
TELEGRAM_TOKEN=123456789:ABCDEF...
TELEGRAM_CHAT_ID=987654321
```
> [!WARNING]
> *(Tekan **Ctrl+X**, lalu **Y**, dan **Enter** untuk menyimpan).*

## 🏃 4. Uji Coba (Pre-Flight Check)

Sebelum menjalankan sebagai layanan *background*, mari kita uji apakah konfigurasi Anda sudah benar.</br>

1. **Aktifkan *Virtual Environment***:
```bash
source venv/bin/activate
```

2. **Jalankan TME-CORE `Doctor` & `Engine`**:
```bash
python3 -m src.main_engine
```
> [!IMPORTANT]
> Jika Anda melihat pesan **"[+] TME-CORE Engine siap menahan serangan!"**, berarti instalasi Anda sukses! Tekan **`Ctrl+C`** untuk mematikan.

## ⚙️ 5. Menjalankan Sebagai Layanan 24/7 (Systemd)

Agar TME-CORE tetap berjalan meskipun terminal ditutup, jadikan sebagai *Service*.</br>

1. Buat file **`service`**:</br>
```bash
sudo nano /etc/systemd/system/tmecore.service
```
2. Isi dengan konfigurasi berikut (Sesuaikan **`/home/teungku/`** dengan *path user* Linux Anda):
```config
[Unit]
Description=TME-CORE MikroTik Mitigation Engine
After=network-online.target

[Service]
Type=simple
User=teungku
WorkingDirectory=/home/teungku/TME-CORE
EnvironmentFile=/home/teungku/TME-CORE/.env
Environment=PYTHONUNBUFFERED=1
ExecStart=/home/teungku/TME-CORE/venv/bin/python -m src.main_engine
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

3. Terapkan dan Nyalakan:
```bash
sudo systemctl daemon-reload
```
```bash
sudo systemctl enable --now tmecore.service
```

4. **Cek Log Langsung**: 
```bash
sudo journalctl -u tmecore.service -f
```
## 📂 6. Manajemen Data & Log

TME-CORE secara otomatis menyusun data operasi Anda di dalam folder **`data/`**:

- **`data/logs/tmecore_system.log`** : Mencatat riwayat operasional engine (kapan `nyala/mati/error`).</br>

- **`data/metrics/evaluasi_kinerja.csv`** : Metrik evaluasi `CPU` dan `RAM` untuk keperluan analisis.</br>

- **`data/db/tme_state.json`** : Ingatan jangka panjang (IP yang sedang diblokir).</br>
