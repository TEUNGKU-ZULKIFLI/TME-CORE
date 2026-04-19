# TME-CORE (Traffic Mitigation External Core)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![GitHub Issues](https://img.shields.io/github/issues/TEUNGKU-ZULKIFLI/TME-CORE?color=red)](https://github.com/TEUNGKU-ZULKIFLI/TME-CORE/issues)
[![NDLC Status](https://img.shields.io/badge/NDLC-Phase%201--3-brightgreen)](https://github.com/TEUNGKU-ZULKIFLI/TME-CORE/issues/1)

---

## 📖 **DAFTAR ISI**

- [Pengantar](#pengantar)
- [Fitur Utama](#fitur-utama-dual-path-detection)
- [Arsitektur & Teknologi](#arsitektur--teknologi)
- [Metrik Evaluasi](#metrik-evaluasi-ndlc)
- [Quick Start](#quick-start)
- [Prasyarat](#prasyarat)
- [Instalasi](#instalasi)
- [Konfigurasi](#konfigurasi)
- [Menjalankan Sistem](#menjalankan-sistem)
- [Struktur Project](#struktur-project)
- [Kontribusi](#kontribusi)
- [Resources](#resources--documentation)

---

## 🎯 **PENGANTAR**

**TME-CORE** adalah sistem mitigasi keamanan otonom berbasis Python yang dirancang untuk melindungi infrastruktur **MikroTik RouterOS** dari serangan Brute Force masif pada layanan SSH (Port 22) dan FTP (Port 21).

### 🔑 **Konsep Utama: Offloading Processing**

Alih-alih membebani CPU router dengan analisis log yang kompleks, sistem ini memindahkan beban pemrosesan ke **External Engine** (Server Debian) yang dedicated, sehingga:
- ✅ Router tetap responsif untuk traffic pengguna
- ✅ Deteksi serangan lebih cepat & akurat
- ✅ Respons mitigasi < 5 detik
- ✅ Scalable untuk infrastruktur enterprise

---

## ✨ **FITUR UTAMA (DUAL-PATH DETECTION)**

Sistem menggunakan mekanisme deteksi **HYBRID** dengan 2 jalur paralel:

### 🔐 **JALUR A: Brute Force Detection**
- **Trigger:** ≥10 kegagalan login dalam 1 menit
- **Aksi:** Blokir IP di firewall address-list secara otomatis
- **Metode:** API MikroTik (port 8728)
- **Alert:** Telegram Bot dengan latensi < 7 detik

### 📈 **JALUR B: Anomaly Detection**
- **Trigger:** Login sukses + CPU spike anomali pasca-autentikasi
- **Aksi:** Blokir IP (suspected malware/backdoor)
- **Analisis:** Behavioral pattern matching
- **Alert:** Telegram Bot dengan context lengkap

### 🤖 **AUTONOMOUS MITIGATION**
- Dynamic firewall rule generation
- Real-time address-list updates
- Automatic remediation tanpa human intervention
- **Mean Time To Respond (MTTR): < 5 detik**

### 📡 **REAL-TIME ALERTING**
- Notifikasi instan ke Telegram
- Include: Threat type, Source IP, Action taken, Timestamp
- Target latensi: < 7 detik

---

## 🛠️ **ARSITEKTUR & TEKNOLOGI**

### 🏗️ **Diagram Sistem**
```
MikroTik Router (SSH/FTP/API)
        ↓ API Connection (port 8728)
Debian Server (External Engine)
  ├─ Log Parser
  ├─ Threat Detection
  ├─ Firewall Manager
  └─ Alert System → Telegram
```

### 🔧 **Tech Stack**

| Komponen | Teknologi | Versi | Fungsi |
|----------|-----------|-------|--------|
| **Engine** | Python | 3.12+ | Logic engine utama |
| **API Client** | RouterOS-api | 0.21.0 | Komunikasi MikroTik |
| **Configuration** | python-dotenv | Latest | Credential management |
| **Alerting** | Telegram Bot | v1.0 | Real-time notification |
| **Target Device** | MikroTik RouterOS | v6.43+ | Perangkat yang dilindungi |

---

## 📊 **METRIK EVALUASI (NDLC)**

Framework **Network Development Life Cycle (NDLC)** dengan 6 fase:

| Metrik | Target | Deskripsi |
|--------|--------|-----------|
| **MTTR** | < 5 detik | Mean Time to Respond |
| **ADR** | 100% | Attack Detection Rate |
| **CPU Offload** | > 60% | Beban CPU router berkurang |
| **Network Stability** | Optimal | Latency & packet loss normal |
| **Alert Latency** | < 7 detik | Telegram notification |

**Status Project:** Phase 1-3 (Analysis → Design → Simulation) | [Lihat Issues](https://github.com/TEUNGKU-ZULKIFLI/TME-CORE/issues)

---

## 🚀 **QUICK START** (5 Menit)

```bash
# 1. Clone & setup
git clone https://github.com/TEUNGKU-ZULKIFLI/TME-CORE.git && cd TME-CORE
python3.12 -m venv venv && source venv/bin/activate

# 2. Install & configure
pip install -r requirements.txt
cp .env.example .env && nano .env

# 3. Test & run
python -c "from config import load_config; config = load_config(); print('✅ Valid!')"
python main.py
```

---

## 📋 **PRASYARAT**

### Hardware/Infrastructure
- Router **MikroTik RouterOS v6.43+** (CHR atau hardware fisik)
- Server/PC **Debian 11+** sebagai External Engine
- Network connectivity antara router dan server

### Software
- **Python 3.12+** - `python3 --version`
- **pip** package manager
- **Git** version control

### Network/API
- API service aktif: `/ip service set api port=8728 disabled=no`
- Firewall rule memperbolehkan port 8728 (Debian → Router)
- User dengan API access di MikroTik

### External Services
- **Telegram Bot Token** (dari [@BotFather](https://t.me/botfather))
- **Chat ID Telegram** (dari [@userinfobot](https://t.me/userinfobot))

---

## 💻 **INSTALASI**

### Step 1: Clone Repository
```bash
git clone https://github.com/TEUNGKU-ZULKIFLI/TME-CORE.git
cd TME-CORE
```

### Step 2: Setup Python Virtual Environment
```bash
python3.12 -m venv venv
source venv/bin/activate  # Linux/Mac
# atau: venv\Scripts\activate  # Windows
```

### Step 3: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Verifikasi:**
```bash
pip list | grep -E "RouterOS|python-dotenv"
```

---

## ⚙️ **KONFIGURASI**

### Step 1: Duplikat Template
```bash
cp .env.example .env
```

### Step 2: Edit `.env` dengan Kredensial Anda
```bash
nano .env
```

**Template `.env` lengkap:**
```env
# ===== MikroTik Router =====
MT_HOST=192.168.88.1
MT_USER=admin
MT_PASS=your_secure_password
MT_PORT=8728

# ===== Telegram Bot =====
TELE_TOKEN=123456789:ABCdefGHI...
CHAT_ID=1234567890

# ===== System =====
LOG_LEVEL=INFO
ALERT_THRESHOLD=10
TIME_WINDOW=60
```

### Step 3: Verifikasi
```bash
python -c "from config import load_config; config = load_config(); print('✅ OK')"
```

---

## ▶️ **MENJALANKAN SISTEM**

```bash
# Mode normal
python main.py

# Mode debug
python main.py --debug

# Mode simulation (testing)
python main.py --simulation

# Monitor logs
tail -f logs/tme-core.log
```

---

## 📁 **STRUKTUR PROJECT**

```
TME-CORE/
├── README.md                    # Dokumentasi
├── BEGINNERS.md                 # Panduan pemula
├── CONTRIBUTING.md              # Contribution guidelines
├── requirements.txt             # Dependencies
├── .env.example                 # Environment template
├── .gitignore                   # Git rules
│
├── main.py                      # Entry point
├── config.py                    # Configuration
│
├── modules/
│   ├── mikrotik_api.py         # API client
│   ├── log_parser.py           # Log parser
│   ├── threat_detector.py      # Detection engine
│   ├── firewall_manager.py     # Firewall manager
│   └── telegram_alert.py       # Alert system
│
├── tests/                       # Unit tests
├── docs/                        # Documentation
└── logs/                        # Runtime logs (gitignored)
```

---

## 🤝 **KONTRIBUSI**

Lihat [CONTRIBUTING.md](CONTRIBUTING.md) untuk guidelines.

**Semantic Commit Format:**
```
<type>(<scope>): <emoji> <subject>
```

**Types:** feat, fix, docs, style, refactor, test, chore
**Scopes:** analysis, design, simulation, implementation, monitoring, management

---

## 📚 **RESOURCES & DOCUMENTATION**

- 📖 [Panduan Pemula](BEGINNERS.md) - Untuk yang baru mulai
- 🤖 [AI Assistant Skills](.github/SKILL.md) - Untuk Vibes Coders
- 🛠️ [Physical Router Setup](docs/PHYSICAL_ROUTER_SETUP.md) - Untuk RB750Gr2
- 🧪 [Baseline Runbook](docs/BASELINE_RUNBOOK.md) - Checklist pengukuran awal
- 🔗 [MikroTik API](https://wiki.mikrotik.com/wiki/Manual:API)
- 🐍 [RouterOS-api Library](https://github.com/socialengineer/python-routeros)
- 💬 [Telegram Bot API](https://core.telegram.org/bots/api)

---

## 📜 **LICENSE**

MIT License - [Lihat LICENSE](LICENSE)

---

**Status:** NDLC Phase 1-3 | **Last Updated:** April 2026