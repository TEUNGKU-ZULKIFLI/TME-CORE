<h1 align="center">
  <img src="https://img.shields.io/badge/🗑️_UNINSTALL_with-TME--CORE-red?style=for-the-badge" />
</h1>

Dokumen ini memandu Anda untuk membersihkan sistem TME-CORE, berkas konfigurasi, serta aturan *firewall* pada *router* target secara aman dan menyeluruh.

## 🧹 Langkah 1: Menghapus Layanan di Server Debian
Jika TME-CORE dipasang sebagai layanan latar belakang (*system service*), lakukan penghentian dan penghapusan layanan dari sistem operasi Debian Anda:

1. Hentikan layanan TME-CORE yang sedang berjalan:
   ```bash
   sudo systemctl stop tmecore.service
   ```

2. Nonaktifkan layanan dari *startup* otomatis:
   ```bash
   sudo systemctl disable tmecore.service
   ```

3. Hapus berkas unit layanan *systemd*:
   ```bash
   sudo rm /etc/systemd/system/tmecore.service
   ```

4. Muat ulang *daemon* sistem untuk menyegarkan konfigurasi:
   ```bash
   sudo systemctl daemon-reload
   ```

## 🧹 Langkah 2: Menggunakan Skrip Pembersih Otomatis
TME-CORE menyediakan skrip pembersih `uninstall.sh` di direktori utama proyek untuk menghapus lingkungan virtual, berkas konfigurasi `.env`, dan struktur folder log/data secara otomatis:

1. Berikan hak izin eksekusi pada skrip pembersih:
   ```bash
   chmod +x uninstall.sh
   ```

2. Jalankan proses pembersihan total:
   ```bash
   source uninstall.sh
   ```

> **⚠️ PERHATIAN:** Skrip ini akan menghapus folder `venv/`, berkas kredensial `.env`, dan *database* status persisten `tme_state.json`. Pastikan Anda telah mencadangkan (*backup*) berkas metrik `evaluasi_kinerja.csv` di folder `data/metrics/` jika Anda masih membutuhkannya untuk pengolahan statistik dan grafik Bab IV skripsi Anda.

## 🧹 Langkah 3: Membersihkan Konfigurasi MikroTik (RouterOS)
Agar *router* MikroTik target kembali ke kondisi semula sebelum eksperimen, lakukan pembersihan manual pada aturan *firewall*:

1. **Hapus Aturan Firewall Filter:**
   Masuk ke Winbox, navigasikan ke menu **IP > Firewall > Filter Rules**. Cari aturan yang men-*drop* paket dari daftar `brute_force_block` (mitigasi Jalur A) atau IP yang diisolasi oleh fitur *Zero Trust* (Jalur B), lalu hapus (*remove*).

2. **Hapus Aturan Firewall Address-List:**
   Buka menu **IP > Firewall > Address Lists**. Hapus semua daftar alamat IP penyerang yang pernah diblokir oleh TME-CORE.

3. **(Opsional) Matikan Layanan API:**
   Jika layanan API port 8728 tidak lagi digunakan oleh aplikasi lain, Anda sangat disarankan untuk menonaktifkannya kembali demi alasan pengerasan keamanan perangkat (*device hardening*):
   ```routeros
   /ip service disable api
   ```
