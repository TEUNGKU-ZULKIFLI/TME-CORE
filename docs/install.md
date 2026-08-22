<h1 align="center">
  <img src="https://img.shields.io/badge/📥_INSTALLASI_with-TME--CORE-green?style=for-the-badge" />
</h1>

Panduan ini menjelaskan prosedur instalasi **TME-CORE** di server pengontrol eksternal berbasis Linux Debian/Ubuntu secara rinci.

## 📋 Prasyarat Sistem (Prerequisites)
Sebelum melanjutkan proses instalasi, pastikan infrastruktur laboratorium atau produksi Anda memenuhi kriteria berikut:

1. **Sisi Server Pengendali (Debian/Ubuntu Server)**
    - **Sistem Operasi**: Debian 11/12 (Direkomendasikan) atau Ubuntu Server 20.04/22.04 LTS.
    - **Python Runtime**: Python versi 3.8 atau yang lebih baru (`Python >= 3.8`).
    - **Soket Jaringan**: Port biner API MikroTik (Port default `8728`) harus dapat dijangkau dari server ini.

2. **Sisi Perangkat Target (MikroTik RouterOS)**
    - **Perangkat Keras**: Semua varian RouterBoard (Teruji secara komprehensif pada [<kbd>`RB941-2nD-TC`](https://mikrotik.com/product/RB941-2nD-TC), [<kbd>`RB750r2`](https://mikrotik.com/product/RB750r2), dan [<kbd>`RB951G-2HnD`](https://mikrotik.com/product/RB951G-2HnD)).
    - **Versi Sistem Operasi**: RouterOS v6.x (Long-term/Stable) atau RouterOS v7.x.
    - **Aktivasi Layanan**: API Service wajib diaktifkan.

## 🛠️ Langkah-Langkah Instalasi
1. **Persiapan Konektivitas MikroTik**
Pastikan Anda telah mengaktifkan layanan API di router MikroTik target. Masuk ke terminal MikroTik Anda (via Winbox atau SSH) dan jalankan perintah berikut:
    - Mengaktifkan layanan API port biner default 8728:
    ```routeros
    /ip service enable api
    ```

    - *(Opsional namun direkomendasikan)* Membatasi akses API hanya dari alamat IP server Debian untuk lapisan keamanan tambahan:
    ```routeros
    /ip service set api address=192.168.10.2/32
    ```

2. **Kloning Repositori TME-CORE**
    - **Menggunakan `SSH`**:
    ```bash
    git clone git@github.com:TEUNGKU-ZULKIFLI/TME-CORE.git
    ```

    - **Atau menggunakan `HTTP`**:
    ```bash
    git clone https://github.com/TEUNGKU-ZULKIFLI/TME-CORE.git
    ```

3. **Eksekusi Skrip Instalasi Otomatis (Auto-Installer)**
TME-CORE telah dilengkapi dengan skrip otomatisasi `install.sh` untuk menyiapkan seluruh dependensi lingkungan Python dengan aman:
    - Masuk ke direktori proyek dan berikan izin eksekusi pada skrip:
    ```bash
    cd TME-CORE
    chmod +x install.sh
    ```
    - Jalankan instalasi menggunakan perintah `source`:
    ```bash
    source install.sh
    ```
   > **💡 Apa yang Dilakukan oleh Skrip `install.sh`?**
   > 1. Membuat lingkungan Python terisolasi (*Virtual Environment*) di direktori `venv/`.
   > 2. Memperbarui manajer pustaka `pip` ke versi terbaru.
   > 3. Memasang pustaka pihak ketiga yang terdaftar pada `requirements.txt` (seperti `routeros_api`, `requests`, `python-dotenv`).
   > 4. Menyalin berkas *template* `.env.example` menjadi berkas konfigurasi aktif `.env`.

<h3>Installasi Cast</h3>
<div id="installasi" class="cast-player"></div>

## 🔍 Verifikasi Struktur Direktori Data
Setelah instalasi selesai, sistem akan membentuk struktur penyimpanan data lokal untuk mendukung operasional dan ekspor metrik penelitian Anda pada direktori `TME-CORE/data/`:
```text
TME-CORE/data/
├── db/          # Menyimpan database persistensi tme_state.json (Manajemen Hitungan & State)
├── logs/        # Menyimpan berkas historis tmecore_system.log
└── metrics/     # Menyimpan dataset evaluasi_kinerja.csv (Relasional Kinerja & Anomali)
```

Jika struktur di atas telah terbentuk dengan lengkap, Anda siap melangkah ke tahap konfigurasi dan pengujian pertama di berkas [Getting Started](getting_started.md).
