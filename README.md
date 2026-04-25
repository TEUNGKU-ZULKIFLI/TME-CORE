# TME-CORE: MikroTik Threat Mitigation Engine

## Deskripsi
Sistem mitigasi otomatis serangan Brute Force SSH/FTP pada Router MikroTik dengan engine eksternal berbasis Python. Engine berjalan di server Debian dan menganalisa log secara real-time, mendeteksi anomali, dan melakukan blocking otomatis via API RouterOS dengan latency < 5 detik.

## Arsitektur
- **Target**: MikroTik RouterOS 6.49.19 (port 21/FTP, 22/SSH, 8728/API)
- **Engine**: Python pada Debian Server
- **Attacker**: Kali Linux (simulasi brute force dengan Hydra/Medusa)
- **Monitoring**: CPU router, failed login attempts, response time

## Metodologi
NDLC (Need, Design, Logical, Complete) untuk siklus pengembangan sistematis dan dokumentasi skripsi.

## Setup Lab
Lihat `docs/setup_lab.md` untuk panduan lengkap.

## Status
🔄 Development in progress (NDLC: Initiation phase)
