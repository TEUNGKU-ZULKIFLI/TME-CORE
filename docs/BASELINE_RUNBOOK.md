# Baseline Runbook (Lab Day)

Panduan ini dipakai untuk pengukuran pertama sebelum coding TME-CORE.

## 1. Tujuan
- Membuat baseline jaringan normal.
- Memastikan Debian WSL bisa berkomunikasi dengan MikroTik fisik.
- Menyiapkan data pembanding sebelum uji brute force terkontrol.

## 2. Prasyarat Sebelum Berangkat ke Lab
- Router fisik RB750Gr2 sudah dipassword.
- API MikroTik aktif dan dibatasi ke IP controller.
- Kabel dan adaptor tersedia.
- WSL Debian dan WSL Kali siap dipakai.
- Spreadsheet atau file catatan siap untuk mencatat hasil.

## 3. Urutan Kerja di Lab
### Langkah 1: Cek perangkat
- Nyalakan router.
- Pastikan lampu port sesuai topologi.
- Pastikan IP router sudah diketahui.

### Langkah 2: Cek konektivitas dasar
Dari Debian WSL:
```bash
ping -c 4 <IP_ROUTER>
```

### Langkah 3: Cek port API
```bash
nc -zv <IP_ROUTER> 8728
```

### Langkah 4: Cek informasi sistem
Jika login RouterOS sudah tersedia:
```rsc
/system resource print
/ip service print
```

### Langkah 5: Catat baseline normal
Lakukan minimal 3 kali pengukuran:
- Latency
- Packet loss
- Throughput
- CPU router
- API response time

### Langkah 6: Simpan bukti
Simpan:
- Screenshot hasil terminal
- Catatan waktu pengukuran
- CSV hasil pengukuran
- Konfigurasi topologi singkat

## 4. Format Catatan Manual
Gunakan format berikut:

```text
Run ID:
Tanggal/Waktu:
Router Model:
RouterOS Version:
Debian Controller IP:
Kali Source IP:
Latency Avg:
Latency p95:
Packet Loss:
Throughput:
CPU Avg:
CPU p95:
API Response Time:
Catatan:
```

## 5. Kriteria Baseline Valid
- Minimal 3 run normal.
- Nilai antar-run tidak ekstrem.
- Tidak ada disconnect API.
- Koneksi Debian ke router stabil.

## 6. Catatan Keamanan
- Jangan jalankan serangan di luar lab berizin.
- Jangan push credential ke repo.
- Jika password admin belum ada, set dulu sebelum pengujian.
