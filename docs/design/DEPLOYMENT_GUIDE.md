# Deployment Guide - TME-CORE Engine Setup

## Prerequisites

- Debian 12 Bookworm
- Python 3.11+
- MikroTik RouterOS 6.49+ dengan API enabled
- Network connectivity: Debian ↔ MikroTik

## Step 1: Environment Setup

```bash
# Clone repository
git clone https://github.com/TEUNGKU-ZULKIFLI/TME-CORE.git
cd TME-CORE

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Configuration

```bash
# Copy template
cp config/.env.example config/.env

# Edit .env dengan credentials MikroTik
nano config/.env
# Edit app_config.yaml jika perlu custom paths
nano config/app_config.yaml
```

## Step 3: Syslog Forwarding
### Step 3.1: Syslog Forwarding (MikroTik)
```mikrotik
/system/logging/action
add name=SendLogtoDebianEngine target=remote remote=192.168.10.2 remote-port=514

/system/logging
set action=SendLogtoDebianEngine topics=warning numbers=2
set action=SendLogtoDebianEngine topics=error number=1
```
### Step 3.1: Syslog Forwarding (Debian Server)
> Update kernel
```bash
sudo apt update && sudo apt upgrade -y
```
> Memeriksa packet
```bash
dpkg -l | grep rsyslog
```
> Menginstall packet
```bash
sudo apt install rsyslog -y
```
> Memeriksa status packet
```bash
sudo systemctl status rsyslog
```
> Config packet dan mengaktifkan provider UDP syslog
```bash
sudo nano /etc/rsyslog.conf
```
> cari baris code
```conf
# provides UDP syslog reception
module(load="imudp")
input(type="imudp" port="514")
```
> Membuat file baru (path log diterima dari mikrotik)
```bash
sudo nano /etc/rsyslog.d/23-remote-incoming.conf
```
> Menambahkan script
```conf
# Redirect MikroTik logs ke /home/<username>/TME-CORE/data/logs/514MikroTik.log
:fromhost-ip,isequal,"192.168.10.1" /home/<username>/TME-CORE/data/logs/514MikroTik.log
```
> Mengatur perizinan file log tersebut
```bash
sudo chown root:<username> data/logs/514MikroTik.log
sudo chmod 640 data/logs/514MikroTik.log
```

## Step 4: Start Engine

```bash
# Method 1: Direct
python3 src/engine.py

# Method 2: Using wrapper script
./run_engine.sh

# Method 3: Daemonize (systemd service)
# TODO: Create systemd unit file
```

## Step 5: Monitoring

```bash
# Check metrics
cat data/metrics/engine_metrics.csv

# Monitor logs
tail -f data/logs/514MikroTik.log

# Check blocked IPs
ssh admin@192.168.10.1 "ip firewall address-list print"
```

## Troubleshooting

### Engine tidak terkoneksi ke MikroTik
- Check: `ping 192.168.10.1`
- Verify: API port 8728 open di firewall
- Check credentials di config/.env

### Logs tidak masuk
- Verify syslog forwarding di MikroTik
- Check rsyslog listening: `sudo ss -ulnp | grep 514`
- Verify log file path: `ls -la data/logs/`

### Engine crash
- Check Python version: `python3 --version` (needs 3.11+)
- Check dependencies: `pip list`
- Check logs: Cek stack trace di stdout