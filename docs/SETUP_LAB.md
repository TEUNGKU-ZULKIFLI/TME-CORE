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
   - Network: ≥2 interfaces

3. **KALI LINUX (Attacker)**
   - RAM: 2GB
   - Storage: 15GB
   - Network: Bridge to MikroTik network

---

## Step 1: Persiapan MikroTik

### 1.1 - Verifikasi Status RouterOS

```bash
# SSH ke MikroTik:
ssh admin@192.168.10.1
# Password: <your-password>

# Cek versi:
[admin@MikroTik] > system/resource/print
                   version: 6.49.19

# Cek interfaces:
[admin@MikroTik] > interface/print

# Cek services (pastikan SSH, FTP, API aktif):
[admin@MikroTik] > ip/service/print
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

```bash
# Buat address-list untuk brute_force_block (jika belum ada):
[admin@MikroTik] > ip/firewall/address-list/add address=0.0.0.0/32 list=brute_force_block comment="Placeholder - auto-populated by TME-CORE"

# Verify:
[admin@MikroTik] > ip/firewall/address-list/print
 #   ADDRESS          LIST                COMMENT
 0   0.0.0.0/32       brute_force_block   Placeholder...
```

### 1.3 - Setup Firewall Filter untuk Blocking

```bash
# Buat rule: DROP traffic dari brute_force_block list
[admin@MikroTik] > ip/firewall/filter/add chain=input src-address-list=brute_force_block action=drop comment="Drop brute_force_block - TME-CORE"

# Verify:
[admin@MikroTik] > ip/firewall/filter/print
 #  CHAIN   SRC-ADDR-LIST        ACTION
 0  input   brute_force_block    drop
```

### 1.4 - Test API Connection

```bash
# Dari Debian, test API connection:
telnet 192.168.10.1 8728

# Expected: Connected
# Ctrl+C untuk exit

# Atau gunakan Python (nanti):
python3 -c "from src.api.mikrotik_client import MikroTikClient; ..."
```

---

## Step 2: Setup Debian Server

### 2.1 - Install Dependencies

```bash
# Login ke Debian:
ssh teungku@192.168.12.1  # (NIC1: Host-only)

# Update system:
sudo apt update && sudo apt upgrade -y

# Install required packages:
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
git clone https://github.com/TEUNGKU-ZULKIFLI/TME-CORE.git
cd TME-CORE

# Checkout branch refactor/ndlc-structure
git checkout refactor/ndlc-structure
```

### 2.3 - Setup Python Virtual Environment

```bash
# Create venv
python3 -m venv venv

# Activate
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep routeros-api
# Output: routeros-api          0.21.0
```

### 2.4 - Configure Environment

```bash
# Copy .env template
cp config/.env.example config/.env

# Edit .env dengan credentials MikroTik Anda:
nano config/.env

# Content:
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

```bash
# Ping MikroTik (ether2: 192.168.10.1)
ping 192.168.10.1 -c 4

# Expected output:
# PING 192.168.10.1 (192.168.10.1) 56(84) bytes of data.
# 64 bytes from 192.168.10.1: icmp_seq=1 time=1.2 ms
# ...
# 0% packet loss
```

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

# Make executable
chmod +x scripts/test_api_connection.py
```

### 3.2 - Run Test

```bash
cd ~/TME-CORE
source venv/bin/activate

python3 scripts/test_api_connection.py

# Expected output:
# INFO:__main__:🔌 Connecting to MikroTik: 192.168.10.1...
# INFO:__main__:✅ Connection successful!
# INFO:__main__:📋 Fetching interfaces...
# INFO:__main__:  - ether1-ISP: ether
# INFO:__main__:  - ether2: ether
# INFO:__main__:✅ All tests passed!
```

---

## Step 4: Verify Log Files

### 4.1 - Check SSH Log

```bash
# SSH ke MikroTik dan trigger failed login:
ssh admin@192.168.10.1
# Enter wrong password 3x

# Kemudian check log:
telnet 192.168.10.1 22
# Or use Kali with Hydra

# Log should appear in:
cat /var/log/auth.log | grep "Failed password"

# Expected:
# Apr 24 10:15:45 debian sshd[1234]: Failed password for admin from 192.168.1.50
```

### 4.2 - Check FTP Log

```bash
# Enable FTP logging (optional):
# di MikroTik, aktifkan FTP service logging

# Check log:
cat /var/log/vsftpd.log

# Expected:
# Wed Apr 24 10:15:50 2026 [pid 567] 192.168.1.50:12345] LOGIN FAILED. [admin]
```

---

## Step 5: Kali Linux Setup (Attacker)

### 5.1 - Install Hydra

```bash
# SSH ke Kali Linux
ssh root@<kali-ip>

# Install Hydra
apt update
apt install -y hydra

# Verify
hydra --version
```

### 5.2 - Prepare Attack

```bash
# Create wordlist (atau download):
cat > /tmp/wordlist.txt << 'EOF'
password123
admin123
12345678
qwerty
mypassword
EOF

# Test SSH brute force (later, untuk testing phase)
hydra -l admin -P /tmp/wordlist.txt ssh://192.168.10.1
```

---

## Verification Checklist

```
✅ Setup Verification Checklist:

Network:
  ☐ Debian ping MikroTik: 0% packet loss
  ☐ Kali ping MikroTik: 0% packet loss
  ☐ MikroTik interfaces aktif (ether1-ISP, ether2)

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

**Solusi:**
```bash
# Verify network connectivity
ping 192.168.10.1

# Check MikroTik API port
telnet 192.168.10.1 8728

# Check firewall rule di Debian
sudo iptables -L | grep 8728

# Verify MikroTik API enabled
ssh admin@192.168.10.1
[admin@MikroTik] > ip/service/print
# Pastikan API port 8728 aktif (X flag = disabled)
```

### Problem: Failed login attempts not logged

**Solusi:**
```bash
# Enable SSH logging di MikroTik
[admin@MikroTik] > system/logging/add topics=account,info action=disk

# Check log directory
[admin@MikroTik] > file/print
# Pastikan /var/log exist dan writable
```

### Problem: Python import error (routeros-api)

**Solusi:**
```bash
# Reinstall dalam venv
source ~/TME-CORE/venv/bin/activate
pip uninstall routeros-api -y
pip install routeros-api==0.21.0

# Test import
python3 -c "import routeros_api; print(routeros_api.__version__)"
```
