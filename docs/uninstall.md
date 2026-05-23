<p align="center">
  <picture>
    <source media="(prefers-color-scheme: night)" srcset="../assets/logos/TME-logo01.png" />
    <img src="../assets/logos/TME-logo01.png" width="500" />
  </picture>
</p>
<h1 align="center">
  <span><b align="center">🗑️ UNINSTALLASI with TME-CORE</b></span>
</h1>

## Quick Guide
> [!WARNING]
> Sudah membuat service yang barjalan **`24 jam`**

Jalankan `uninstall.sh` dengan `source`
```bash
source uninstall.sh
```

## Manual Guide
Memastikan Engine service berhenti
```bash
sudo systemctl stop tmecore.service
```
Mulai Mematikan Engine service
```bash
sudo systemctl disable tmecore.service
```
Mulai Menghapus Engine service
```bash
sudo rm -rf /etc/systemd/system/tmecore.service
```
Memuat Ulang SystemD
```bash
sudo systemctl daemon-reload
```
Validasi Engine Service
```bash
system status tmecore.service
```