<p align="center">
  <picture>
    <source media="(prefers-color-scheme: night)" srcset="../assets/logos/TME-logo01.png" />
    <img src="../assets/logos/TME-logo01.png" width="500" />
  </picture>
</p>
<h1 align="center">
  <span><b align="center">⌨️ BASIC CLI with TME-CORE</b></span>
</h1>

## **Check Status Engine**
**Pastikan sudah menyetup Systemd:**</br>
<a href="./getting_started.md#%EF%B8%8F-5-menjalankan-sebagai-layanan-247-systemd">
  <img src="https://img.shields.io/badge/⚙️-ENGINE-orange?style=for-the-badge" />
</a></br>

### **Status Engine**
**`Checking Service Engine`**
```bash
sudo systemctl status tmecore.service
```

### **Hidupkan Engine**
**`Starting Service Engine`**
```bash
sudo systemctl start tmecore.service
```

### **Hentikan Engine**
**`Stop it Service Engine`**
```bash
sudo systemctl stop tmecore.service
```

### **Mulai Ulang Engine**
**`Restarting Service Engine`**
```bash
sudo systemctl restart tmecore.service
```

## **CLI (Command Line Interface) Basic**
### **Running Engine**
Aktifkan lingkungan **`Virtual Environment`**
```bash
source venv/bin/activate
```
**`🔥 STARTING ENGINE`**
```bash
python3 -m src.main_engine
```

### **Test Connection**
Aktifkan lingkungan **`Virtual Environment`**
```bash
source venv/bin/activate
```
**`📎 TEST KONEKSI`**
```bash
python3 -m src.api.connection
```

### **Test Log Parser**
Aktifkan lingkungan **`Virtual Environment`**
```bash
source venv/bin/activate
```
**`📃 TEST LOG PARSER`**
```bash
python3 -m src.parser.log_parser
```

### **Test Monitoring CPU & RAM**
Aktifkan lingkungan **`Virtual Environment`**
```bash
source venv/bin/activate
```
**`👀 TEST MONITOR REALTIME CPU & RAM`**
```bash
python3 -m src.monitoring.realtime_cpu_ram
```