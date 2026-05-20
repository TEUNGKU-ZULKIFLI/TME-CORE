<p align="center">
  <picture>
    <source media="(prefers-color-scheme: night)" srcset="./assets/logos/TME-logo01.png" />
    <img src="./assets/logos/TME-logo01.png" width="500" />
  </picture>
</p>
<h1 align="center">
  <span><b align="center">TEUNGKU MITIGATION ENGINE - Core</b></span>
</h1>
<p align="center">
  🚀 <a href="./docs/getting_started.md">Getting Started</a> · 
  📑 <a href="./docs/all-tahap.md">Documentation</a> · 
  ❓ <a href="#apa-itu">Apa itu TME-CORE</a> · 
  ⚙️ <a href="#cara-kerja">Cara Kerja</a> · 
  ✨ <a href="#fitur-utama">Fitur Utama</a> · 
  💻 <a href="#persyaratan-sistem">Persyaratan Sistem</a> · 
  📥 <a href="#installasi">Installasi</a> · 
  🚀 <a href="#panduan-cepat">Panduan Cepat</a> · 
  🗑️ <a href="#uninstallasi">Uninstallasi</a> · 
  🔧 <a href="#troubleshooting">Troubleshooting</a> · 
  🎯 <a href="#tujuan">Tujuan</a> · 
  👤 <a href="#kontribusi">Kontribusi</a> · 
  ⚖️ <a href="#lisensi">Lisensi</a> · 
  📞 <a href="#kontak-support">Kontak / Support</a>
</p>

---

## Apa itu?
**`TME-CORE`** adalah sistem mitigasi otomatis untuk serangan **Brute Force SSH/FTP** pada Router MikroTik.
Engine berbasis **Python** ini berjalan di server Debian, menganalisa log secara real-time, mendeteksi anomali, dan melakukan blocking otomatis via API RouterOS dengan latency `< 5 detik` ⚡.

## Cara Kerja
```mermaid
graph TB
    %% Subgraph grouping
    subgraph Attacker
        hacker[<b/>Hydra]
    end

    subgraph Defense
        router[<b/>MikroTik RouterOS]
        server[<b/>Debian Server]
        engine[<b/>TME Core Service]
    end

    subgraph Notification
        bot[<b/>Bot Telegram]
    end

    %% Flow
    hacker -- 🔴 SSH/FTP brute force --> router
    router -- 🔗 API port 8728 --> server
    server -- ⚙️ Activate 24/7 --> engine
    engine -- ⚠️ Threshold reached --> router
    engine -- 🛡️ Blocked attacker --> hacker
    engine -- 🔔 Send notif --> bot

    %% Node styling
    style hacker fill:#cc0000,stroke:#660000,stroke-width:2px,color:#ffffff
    style router fill:#33cc33,stroke:#006600,stroke-width:2px,color:#ffffff
    style server fill:#cccccc,stroke:#666666,stroke-width:1.5px,color:#000000
    style engine fill:#ffcc00,stroke:#cc9900,stroke-width:2px,color:#000000
    style bot fill:#3399ff,stroke:#0066cc,stroke-width:2px,color:#ffffff

    %% Subgraph styling
    style Attacker fill:#ffe5e5,stroke:#cc0000,color:#000000
    style Defense fill:#f9f9f9,stroke:#999999,color:#000000
    style Notification fill:#e5f0ff,stroke:#0066cc,color:#000000
```
**Narasi alur**:
- **Attacker** mencoba brute force ke port SSH/FTP router.
- **Router** meneruskan log ke server.
- **Server** menjalankan TME-Core 24 jam nonstop.
- **Engine** mendeteksi percobaan gagal, menunggu hingga mencapai threshold.
- Jika threshold tercapai, engine mengirim perintah blokir ke router dan feedback ke attacker.
- Engine juga mengirim **notifikasi** ke Bot Telegram bahwa serangan berhasil ditangani.

## Fitur Utama
- 🔎 Analisis log real-time
- 🛡️ Deteksi brute force otomatis
- ⚡ Blocking cepat via API
- 🔗 Integrasi langsung dengan RouterOS
- 📨 Pesan dari Bot Telegram

## Persyaratan Sistem
- 🛜 Router MikroTik
- 💻 Server/VPS
- 🐍 Python version 3.xx

## Installasi
<a href="./docs/install.md">
  <img src="https://img.shields.io/badge/📥-Install-green?style=for-the-badge" />
</a>

## Panduan Cepat
**TME-CORE** dapat diinstal di Linux Debian/Ubuntu (Server Lokal maupun Cloud VPS).</br>

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

<a href="./docs/getting_started.md">
  <img src="https://img.shields.io/badge/🚀-Getting%20Started-blue?style=for-the-badge" />
</a>

## Uninstallasi
<a href="./docs/uninstall.md">
  <img src="https://img.shields.io/badge/🗑️-Uninstall-red?style=for-the-badge" />
</a>

## Troubleshooting
<a href="./docs/troubleshooting.md">
  <img src="https://img.shields.io/badge/🔧-Troubleshooting-orange?style=for-the-badge" />
</a>

## Tujuan
Memberikan perlindungan ekstra pada Router MikroTik dengan cara yang **ringan, cepat, dan menyenangkan** untuk sysadmin yang ingin tidur lebih nyenyak 😴.

## Kontribusi

## Lisensi

## Kontak Support
