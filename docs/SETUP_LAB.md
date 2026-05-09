# Panduan Setup Lab Virtual TME-CORE

## Prasyarat

### Hardware/Host
- **OS Host**: Windows 11 Pro (Hyper-V) atau VMware/VirtualBox
- **RAM**: ≥8GB untuk host
- **Storage**: ≥50GB free
- **Network**: Static IP atau DHCP untuk VMs

### VMs yang Diperlukan

1. **DEBIAN 12 Bookworm (Server Engine)**
   - RAM: 2GB
   - Storage: 20GB
   - Network: 2 NICs (Host-only + Bridge/Direct)

2. **MikroTik RouterOS 6.49.19** (Real Hardware atau VM)
   - RAM: 256MB minimal
   - Storage: On-board (hEX = 16MB)
   - Network: ≥3 interfaces

3. **KALI LINUX (Attacker)**
   - RAM: 2GB
   - Storage: 15GB
   - Network: 2 NICs (Host-only + Bridge/Direct)

---

## Step 1: Persiapan MikroTik

### 1.1 - Verifikasi Status RouterOS

> [!WARNING]
> SSH ke MikroTik Jika dengan PowerShell:
```bash
ssh -o MACs=hmac-sha1 admin@192.168.10.1
```
> Cek versi:
```bash
[admin@MikroTik] > system resource print
                   version: 6.49.19
```
> Cek interfaces:
```bash
[admin@MikroTik] > interface print
```

> [!WARNING]
>  Cek services (pastikan SSH, FTP, API aktif):
```bash
[admin@MikroTik] > ip service print
Flags: X - disabled
 #   NAME       PORT
 0   telnet      23
 1   ftp         21     ◄── Aktif
 2   www         80
 3   ssh         22     ◄── Aktif
 4   api       8728     ◄── Aktif (penting!)
 5   winbox    8291
```

### 1.2 - Setup Address-List untuk Blocking

> [!TIP]
> Buat address-list untuk brute_force_block (jika belum ada):
```bash
[admin@MikroTik] > ip firewall address-list add address=0.0.0.0/32 list=brute_force_block comment="Placeholder - auto-populated by TME-CORE"
```
> Verify:
```bash
[admin@MikroTik] > ip firewall address-list print
```
> *Expected:*
> > #ADDRESS          LIST                COMMENT
> 0   0.0.0.0/32       brute_force_block   Placeholder...

### 1.3 - Setup Firewall Filter untuk Blocking

> [!TIP]
> Buat rule: DROP traffic dari brute_force_block list
```bash
[admin@MikroTik] > ip firewall filter add chain=input src-address-list=brute_force_block action=drop comment="Drop brute_force_block - TME-CORE"
```
> Verify:
```bash
[admin@MikroTik] > ip firewall filter print
```
> *Expected:*
> > \# CHAIN   SRC-ADDR-LIST        ACTION
> 0  input   brute_force_block    drop

### 1.4 - Test API Connection

> [!TIP]
> Dari Debian, test API connection:
```bash
telnet 192.168.10.1 8728

# Expected: Connected
# Ctrl+C untuk exit

# Atau gunakan Python (nanti):
python3 -c "from src.api.mikrotik_client import MikroTikClient; ..."
```

---

## Step 2: Setup Debian Server

### 2.1 - Install Dependencies

> Login ke Debian:
```bash
ssh teungku@192.168.12.1  # (NIC1: Host-only)
```
> Update system:
```bash
sudo apt update && sudo apt upgrade -y
```
> Install required packages:
```bash
sudo apt install -y \
  python3.11 \
  python3-pip \
  python3-venv \
  git \
  openssh-server \
  net-tools \
  curl \
  wget
```

### 2.2 - Clone TME-CORE Repository

```bash
cd ~
```
```bash
git clone https://github.com/TEUNGKU-ZULKIFLI/TME-CORE.git
```
```bash
cd TME-CORE
```

### 2.3 - Setup Python Virtual Environment
> [!IMPORTANT]
> Create venv
```bash
python3 -m venv venv
```
> Activate
```bash
source venv/bin/activate
```
> Upgrade pip
```bash
pip install --upgrade pip
```
> Install dependencies
```bash
pip install -r requirements.txt
```
> Verify installation
```bash
pip list | grep routeros-api
```
> Atau Untuk Check package yang utamanya
```bash
pip install routeros-api
```
> Output: routeros-api          0.21.0

### 2.4 - Configure Environment

> Copy .env template
```bash
cp config/.env.example config/.env
```
> Edit .env dengan credentials MikroTik Anda:
```bash
nano config/.env
```
> Content:
```bash
MIKROTIK_HOST=192.168.10.1
MIKROTIK_USERNAME=admin
MIKROTIK_PASSWORD=<your-password>
MIKROTIK_PORT=8728
MIKROTIK_TIMEOUT=10

LOG_FILE_SSH=/var/log/auth.log
LOG_FILE_FTP=/var/log/vsftpd.log

BF_THRESHOLD=10
BF_WINDOW_SECONDS=60
CPU_SPIKE_THRESHOLD=30

TELEGRAM_BOT_TOKEN=<your-bot-token>  # Setup later
TELEGRAM_CHAT_ID=<your-chat-id>      # Setup later

DEBUG=False
LOG_LEVEL=INFO
```

### 2.5 - Test MikroTik Connectivity

> Ping MikroTik (ether2-DEBIAN: 192.168.10.1)
```bash
ping 192.168.10.1 -c 4
```
> *Expected output:*
> > PING 192.168.10.1 (192.168.10.1) 56(84) bytes of data.
> 64 bytes from 192.168.10.1: icmp_seq=1 time=1.2 ms
> ...
> 0% packet loss

---

## Step 3: Test API Connection Basic

### 3.1 - Buat Test Script

```bash
cat > scripts/test_api_connection.py << 'EOF'
#!/usr/bin/env python3
"""
Simple test untuk API connection ke MikroTik
"""
import sys
sys.path.insert(0, '/home/teungku/TME-CORE')

from src.api.mikrotik_client import MikroTikClient
from src.config import get_config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        config = get_config()
        logger.info(f"🔌 Connecting to MikroTik: {config['mikrotik']['host']}...")
        
        client = MikroTikClient(**config['mikrotik'])
        client.connect()
        
        logger.info("✅ Connection successful!")
        
        # Get interfaces
        logger.info("📋 Fetching interfaces...")
        interfaces = client.execute_command("/interface/print")
        for iface in interfaces:
            logger.info(f"  - {iface.get('name')}: {iface.get('type')}")
        
        # Get CPU
        logger.info("📊 Fetching CPU info...")
        cpu = client.get_router_cpu()
        logger.info(f"  - CPU Load: {cpu['cpu_load']}%")
        logger.info(f"  - Free Memory: {cpu['free_memory_mb']:.1f} MB")
        
        client.disconnect()
        logger.info("✅ All tests passed!")
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
EOF
```
> Make executable
```bash
chmod +x scripts/test_api_connection.py
```

### 3.2 - Run Test

```bash
cd ~/TME-CORE
```
```bash
source venv/bin/activate
```
```bash
python3 scripts/test_api_connection.py
```
> *Expected output:*
> > INFO:__main__:🔌 Connecting to MikroTik: 192.168.10.1...
> INFO:__main__:✅ Connection successful!
> INFO:__main__:📋 Fetching interfaces...
> INFO:__main__:  - ether1-ISP: ether
> INFO:__main__:  - ether2: ether
> INFO:__main__:✅ All tests passed!

---

## Step 4: Verify Log Files

### 4.1 - Check SSH Log
> [!IMPORTANT]
> SSH ke MikroTik dan trigger failed login:
```bash
ssh -o MACs=hmac-sha1 admin@192.168.10.1
```
> Enter wrong password 3x

> Kemudian check log:
```bash
telnet 192.168.10.1 22
```
> [!IMPORTANT]
> Or use Kali with Hydra

> Log should appear in:
```bash
cat /var/log/auth.log | grep "Failed password"
```
> *Expected:*
> > Apr 24 10:15:45 debian sshd[1234]: Failed password for admin from 192.168.1.50

### 4.2 - Check FTP Log

> [!TIP]
> Enable FTP logging (optional):
> di MikroTik, aktifkan FTP service logging

> Check log:
```bash
cat /var/log/vsftpd.log
```
> *Expected:*
> > Wed Apr 24 10:15:50 2026 [pid 567] 192.168.1.50:12345] LOGIN FAILED. [admin]

---

## Step 5: Kali Linux Setup (Attacker)

### 5.1 - Install Hydra

> [!CAUTION]
> SSH ke Kali Linux
```bash
ssh root@192.168.254.1 # (NIC1: Host-only)
```
> Install Hydra
```bash
apt update
```
```bash
apt install -y hydra
```
> Verify
```bash
hydra --version
```

### 5.2 - Prepare Attack

> Create wordlist:
```bash
cat > /tmp/wordlist.txt << 'EOF'
password123
admin123
12345678
qwerty
mypassword
EOF
```
> [!IMPORTANT]
> Atau download wordlist dengan wget:
```bash
wget https://archive.org/download/rockyou.txt/rockyou.txt -O /tmp/wordlist.txt
```
> [!CAUTION]
> Test SSH brute force (later, untuk testing phase)
```bash
hydra -l admin -P /tmp/wordlist.txt ssh://192.168.20.1 -v -I
```

---

## Verification Checklist

```
✅ Setup Verification Checklist:

Network:
  ☐ Debian ping MikroTik: 0% packet loss
  ☐ Kali ping MikroTik: 0% packet loss
  ☐ MikroTik interfaces aktif (ether1-ISP, ether2-DEBIAN, ether3-KALI)

MikroTik:
  ☐ SSH service aktif (port 22)
  ☐ FTP service aktif (port 21)
  ☐ API service aktif (port 8728)
  ☐ address-list brute_force_block exist
  ☐ firewall filter drop rule active

Debian:
  ☐ Python 3.11 installed
  ☐ venv activated
  ☐ requirements.txt installed
  ☐ config/.env configured
  ☐ scripts/test_api_connection.py runs successfully

Kali:
  ☐ Hydra installed
  ☐ SSH access ke MikroTik possible
  ☐ Wordlist prepared
```

---

## Troubleshooting

### Problem: Connection timeout ke MikroTik

> [!IMPORTANT]
> **Solusi:**
> **Verify network connectivity**
```bash
ping 192.168.10.1
```
> **Check MikroTik API port**
```bash
telnet 192.168.10.1 8728
```
> **Check firewall rule di Debian**
```bash
sudo iptables -L | grep 8728
```
> **Verify MikroTik API enabled**
```bash
ssh -o MACs=hmac-sha1 admin@192.168.10.1
```
```bash
[admin@MikroTik] > ip service print
```
> [!WARNING]
> Pastikan API port 8728 aktif (X flag = disabled)

### Problem: Failed login attempts not logged
> [!IMPORTANT]
> **Solusi:**
> **Enable SSH logging di MikroTik**
```bash
[admin@MikroTik] > system logging add topics=account,info action=disk
```
> **Check log directory**
```bash
[admin@MikroTik] > file print
```
> Pastikan /var/log exist dan writable

### Problem: Python import error (routeros-api)
> [!IMPORTANT]
> **Solusi:**
> **Reinstall dalam venv**
```bash
source ~/TME-CORE/venv/bin/activate
```
```bash
pip uninstall routeros-api -y
```
```bash
pip install routeros-api==0.21.0
```
> Test import
```bash
python3 -c "import routeros_api; print(routeros_api.__version__)"
```

### Problem: Brute Force With Hydra tools
*`[ERROR] could not connect to ssh://192.168.20.1:22 - kex error : no match for method mac algo client->server: server [hmac-sha1,hmac-md5], client [hmac-sha2-256-etm@openssh.com,hmac-sha2-512-etm@openssh.com,hmac-sha2-256,hmac-sha2-512]`*

> [!IMPORTANT]
> **Solusi:**
> Mengubah atau memodifikasi ssh kali linux bisa memakai hmac-sha1 juga.
```bash
cd /etc/ssh
```
> Kemudian melihat file config ssh
```bash
ls -la
```
> Pastikan menemukan file: 
`ssh_config` dan membukanya dengan `editor nano`.

> [!WARNING]
> Memodifikasi file config ssh dengan menambahkan skrip berikut:
```bash
# Menambahkan generate ssh dengan HASH MAC-SHA1 ke semua host
Host *
	hmac-sha1,hmac-md5
```
`Ctrl + o` Untuk Simpan `Enter` Kemudian `Ctrl + x` Untuk keluar `editor nano`.

> [!IMPORTANT]
> Setelah itu Coba Brute Force ulang.
