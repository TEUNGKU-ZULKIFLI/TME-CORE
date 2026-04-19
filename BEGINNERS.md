# 👶 PANDUAN PEMULA: TME-CORE

**Buat programmer yang belum pernah tahu tentang MikroTik, Python API, atau threat detection sebelumnya.**

Jangan khawatir! Kami akan jelaskan step-by-step dengan analogi sederhana. 🚀

---

## 📚 DAFTAR ISI

1. [Konsep Dasar](#1-konsep-dasar)
2. [Apa itu MikroTik?](#2-apa-itu-mikrotik)
3. [Apa itu Brute Force?](#3-apa-itu-brute-force)
4. [Bagaimana TME-CORE Bekerja?](#4-bagaimana-tme-core-bekerja)
5. [Setup Awal](#5-setup-awal)
6. [First Run](#6-first-run)
7. [Troubleshooting](#7-troubleshooting)
8. [Next Steps](#8-next-steps)

---

## 1️⃣ KONSEP DASAR

### Analogi: Sistem Keamanan Rumah

```
RUMAH ANDA = MikroTik Router
  ├─ Pintu Depan = Port SSH (22) & FTP (21)
  ├─ Sistem CCTV = TME-CORE Monitoring
  └─ Alarm = Telegram Alert

TAMU JAHAT = Attacker
  └─ Mencoba masuk dengan kunci random

SECURITY GUARD = AI Engine
  ├─ Pantau video CCTV
  ├─ Hitung percobaan masuk gagal
  ├─ Tutup pintu saat ada ancaman
  └─ Hubungi Anda via telepon
```

---

## 2️⃣ APA ITU MIKROTIK?

### Penjelasan Sederhana

**MikroTik** = "Komputer khusus untuk router jaringan"

Ibarat:
- 🏠 Rumah Anda = Jaringan lokal Anda
- 🚪 Pintu masuk/keluar = MikroTik Router
- 👮 Penjaga pintu = Security features MikroTik
- 📱 Telepon di pintu = API MikroTik

### Apa itu RouterOS?

**RouterOS** = Operating system khusus untuk MikroTik (ibarat Windows/Linux tapi untuk router)

### Apa itu API?

**API (Application Programming Interface)** = "Bahasa yang dipahami MikroTik"

Analogi:
```
Anda → Bahasa Indonesia → Teman
Anda → Bahasa Inggris → Bule
Anda → API MikroTik → Router MikroTik

Router: "Kamu mau apa?"
Anda (via API): "Blokir IP 192.168.1.50!"
Router: "OK, sudah di-blokir!"
```

---

## 3️⃣ APA ITU BRUTE FORCE?

### Attack Scenario

Bayangkan Anda punya kunci keamanan PIN di rumah: `1234`

**Attacker mencoba:**
```
Attempt 1: 0000 ❌ SALAH
Attempt 2: 0001 ❌ SALAH
Attempt 3: 0002 ❌ SALAH
...
Attempt 100: 1234 ✅ BENAR! (Masuk!)
```

**Ini adalah BRUTE FORCE:** Mencoba semua kemungkinan sampai ketemu yang benar.

### SSH Brute Force pada MikroTik

```
Attacker → SSH ke 192.168.88.1 port 22
Attacker: "Login dengan username: admin, password: password1"
Router: "Salah!"
Attacker: "Login dengan username: admin, password: password2"
Router: "Salah!"
...
(10+ attempts dalam 1 menit)
Router: "🚨 SERANGAN BRUTE FORCE! TUTUP PINTU!"
```

---

## 4️⃣ BAGAIMANA TME-CORE BEKERJA?

### Flow Diagram (Sangat Sederhana)

```
┌─────────────┐
│ MikroTik    │
│ Router      │
└──────┬──────┘
       │ "Ada failed login nih"
       ↓
┌─────────────┐
│ Debian      │
│ Server      │ ← Ini kami (TME-CORE)
│ (TME-CORE)  │
└──────┬──────┘
       │ "Hitung... hitung... 10+ failed logins!"
       ├─→ Blokir IP di firewall
       ├─→ Kirim alert ke Telegram
       └─→ Log semua kejadian
       ↓
┌─────────────┐
│ Firewall    │
│ (DROP IP)   │
└─────────────┘
       ↓
Admin dapat notifikasi Telegram: "🚨 Blocked: 203.0.113.50 (10 SSH attempts)"
```

### 2 Cara Deteksi

#### Jalur A: Brute Force Detection
```
TRIGGER: "Ada 10+ failed login dalam 1 menit?"
ACTION: Blokir IP itu!
CONTOH:
  203.0.113.1 → ssh attempt 1 FAIL
  203.0.113.1 → ssh attempt 2 FAIL
  203.0.113.1 → ssh attempt 3 FAIL
  ... (10+ times)
  203.0.113.1 → BLOKIR! (DROP)
```

#### Jalur B: Anomaly Detection
```
TRIGGER: "Login berhasil tapi CPU spike aneh?"
ACTION: Ini mungkin malware! Blokir!
CONTOH:
  203.0.113.2 → ssh login SUCCESS (normal)
  Tapi: CPU langsung naik 80% (anomali!)
  KESIMPULAN: Ini suspicious behavior
  ACTION: Blokir 203.0.113.2
```

---

## 5️⃣ SETUP AWAL

### Langkah 1: Cek Python Version

**Kenapa?** TME-CORE perlu Python 3.12+

```bash
python3 --version
```

**Expected output:**
```
Python 3.12.0  ✅ OK
# atau
Python 3.11.0  ❌ Terlalu lama, perlu update
```

### Langkah 2: Buat Folder Project

```bash
mkdir ~/projects
cd ~/projects
git clone https://github.com/TEUNGKU-ZULKIFLI/TME-CORE.git
cd TME-CORE
```

### Langkah 3: Buat Virtual Environment

**Kenapa?** Biar Python packages terisolasi, gak bentrok dengan project lain.

```bash
python3.12 -m venv venv
```

**Ini membuat folder `venv/` dengan Python fresh.** ✨

### Langkah 4: Aktifkan Virtual Environment

**Linux/Mac:**
```bash
source venv/bin/activate
```

**Lihat di terminal:**
```
(venv) user@debian:~/projects/TME-CORE$
        ↑ Ini tandanya venv aktif
```

### Langkah 5: Install Dependencies

```bash
pip install -r requirements.txt
```

**Ini install semua library yang diperlukan:**
- `RouterOS-api` = Untuk komunikasi dengan MikroTik
- `python-dotenv` = Untuk manage credentials

### Langkah 6: Setup Credentials

```bash
# Copy template
cp .env.example .env

# Edit dengan editor favorit
nano .env
```

**File `.env` terlihat seperti:**
```env
MT_HOST=192.168.88.1
MT_USER=admin
MT_PASS=password_anda
MT_PORT=8728
TELE_TOKEN=123456789:ABCdefGHI...
CHAT_ID=1234567890
```

**Apa arti masing-masing?**
| Variable | Arti |
|----------|------|
| `MT_HOST` | IP address router MikroTik Anda |
| `MT_USER` | Username untuk login ke API MikroTik |
| `MT_PASS` | Password untuk login ke API MikroTik |
| `MT_PORT` | Port API (default: 8728) |
| `TELE_TOKEN` | Token bot Telegram (dari @BotFather) |
| `CHAT_ID` | Chat ID Anda (dari @userinfobot) |

---

## 🎁 BONUS: Cara Dapat Token Telegram

### Step 1: Buka @BotFather

Pergi ke [@BotFather](https://t.me/botfather) di Telegram

### Step 2: Create New Bot

```
You: /newbot
BotFather: Okay! Let's create a new bot. How are going to call your bot? Please choose a name for your bot.
You: my-tme-core-bot
BotFather: Good! Now let's choose a username for your bot. It must end in `bot`. For example, TetrisBot or tetris_bot.
You: my_tme_core_bot
BotFather: ✅ Done! Here's your bot info:

Here is your brand new Telegram bot. You will find it at t.me/my_tme_core_bot. You can now add a description, about section and commands. Commands are listed when the user types "/" in the chat with your bot.

Use this token to access the HTTP API:
>>> 123456789:ABCdefGHIjklmnoPQRstuvWXYZ1234567890abc <<<
```

**Copy token ini ke `.env` sebagai `TELE_TOKEN`!**

### Step 3: Get Your Chat ID

1. Buka bot yang baru dibuat: `t.me/my_tme_core_bot`
2. Kirim message: `/start`
3. Pergi ke [@userinfobot](https://t.me/userinfobot)
4. Lihat Chat ID Anda
5. Copy ke `.env` sebagai `CHAT_ID`

---

## 6️⃣ FIRST RUN

### Verifikasi Credentials Benar

```bash
python -c "
from config import load_config
try:
    config = load_config()
    print('✅ Credentials loaded successfully!')
    print(f'   MikroTik Host: {config[\"MT_HOST\"]}')
    print(f'   Telegram Token: {config[\"TELE_TOKEN\"][:20]}...')
except Exception as e:
    print(f'❌ Error: {e}')
"
```

### Test Koneksi ke MikroTik

```bash
python -c "
from routeros_api import Api
from config import load_config

config = load_config()
api = Api(host=config['MT_HOST'], user=config['MT_USER'], password=config['MT_PASS'])
try:
    api.connect()
    print('✅ Connected to MikroTik!')
    api.close()
except Exception as e:
    print(f'❌ Connection failed: {e}')
"
```

### Test Notifikasi Telegram

```bash
python -c "
import requests
from config import load_config

config = load_config()
url = f'https://api.telegram.org/bot{config[\"TELE_TOKEN\"]}/sendMessage'
payload = {
    'chat_id': config['CHAT_ID'],
    'text': '🧪 Test notification dari TME-CORE!'
}

try:
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print('✅ Telegram notification sent!')
    else:
        print(f'❌ Failed: {response.status_code}')
except Exception as e:
    print(f'❌ Error: {e}')
"
```

### Run Sistem

```bash
python main.py
```

**Output yang diharapkan:**
```
2026-04-19 10:30:45 [INFO] TME-CORE Started
2026-04-19 10:30:46 [INFO] Connected to MikroTik router
2026-04-19 10:30:47 [INFO] Listening for threats...
```

---

## 7️⃣ TROUBLESHOOTING

### ❌ Error: "ModuleNotFoundError: No module named 'routeros_api'"

**Penyebab:** Virtual environment tidak aktif atau dependencies belum terinstall

**Solusi:**
```bash
# Pastikan venv aktif
source venv/bin/activate

# Install ulang
pip install -r requirements.txt
```

---

### ❌ Error: ".env file not found"

**Penyebab:** Belum copy `.env.example` ke `.env`

**Solusi:**
```bash
cp .env.example .env
# Edit .env dengan credentials Anda
```

---

### ❌ Error: "Connection refused to 192.168.88.1:8728"

**Penyebab:** 
1. Router tidak online
2. API port 8728 tidak aktif
3. Firewall blocking port 8728

**Solusi:**
```bash
# 1. Ping router
ping 192.168.88.1

# 2. Check MikroTik API status (via SSH/telnet ke router):
ssh admin@192.168.88.1
# di router:
/ip service print
# Pastikan "api" tidak disabled

# 3. Aktifkan API jika disabled:
/ip service set api disabled=no
```

---

### ❌ Error: "Telegram API error: 401 Unauthorized"

**Penyebab:** Token Telegram salah atau expired

**Solusi:**
1. Verifikasi token di `.env` benar (copy dari @BotFather)
2. Pastikan tidak ada space/typo
3. Jika perlu, buat bot baru

---

## 8️⃣ NEXT STEPS

### Langkah Selanjutnya (untuk yang ingin deeper)

#### Level 1: Basic Understanding ✅ (Anda di sini)
- [x] Pahami konsep dasar
- [x] Setup project
- [x] First run berhasil

#### Level 2: Exploration
- [ ] Baca CONTRIBUTING.md (commit guidelines)
- [ ] Eksplor kode yang ada
- [ ] Pahami project structure
- [ ] Baca dokumentasi MikroTik API

#### Level 3: Hands-On
- [ ] Buat branch baru: `git checkout -b feat/explore`
- [ ] Eksperimen dengan code
- [ ] Try modify detection rules
- [ ] Test dengan mock data

#### Level 4: Contribution
- [ ] Pilih issue (#2, #3, atau #4)
- [ ] Implement feature
- [ ] Test thoroughly
- [ ] Buat pull request

---

## 📖 LEARNING RESOURCES

### Untuk Pemula Python
- [Python Official Tutorial](https://docs.python.org/3/tutorial/) - Belajar basic Python
- [Real Python](https://realpython.com/) - Tutorial interaktif

### Untuk Memahami MikroTik
- [MikroTik Official Wiki](https://wiki.mikrotik.com/) - Documentation lengkap
- [MikroTik API Manual](https://wiki.mikrotik.com/wiki/Manual:API) - API reference

### Untuk Memahami Network Security
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) - Security basics
- [SSH Protocol](https://en.wikipedia.org/wiki/Secure_Shell) - Understand SSH

### Untuk Belajar Git
- [Git Official Book](https://git-scm.com/book/en/v2) - Learn Git properly
- [GitHub Hello World](https://guides.github.com/activities/hello-world/) - Quick start

---

## 🎯 QUICK REFERENCE

### Common Commands

```bash
# Activate venv
source venv/bin/activate

# Run system
python main.py

# Check logs
tail -f logs/tme-core.log

# Stop system
Ctrl+C

# Update dependencies
pip install --upgrade -r requirements.txt

# Check version
python --version

# Create new branch (for contribution)
git checkout -b feat/my-feature
```

---

## ❓ QUICK FAQ

**Q: Bisakah saya menjalankan ini di Windows?**
A: Ya! Setup mirip, tapi ganti `source venv/bin/activate` dengan `venv\Scripts\activate`

**Q: Apa yang terjadi jika koneksi ke router putus?**
A: Sistem akan coba reconnect otomatis dan log error. Lihat logs untuk detailnya.

**Q: Bisakah saya test tanpa router asli?**
A: Ya! Gunakan CHR (Cloud Hosted Router) atau simulator. Phase 3 akan cover ini.

**Q: Bagaimana menambah detection rule baru?**
A: Modifikasi `threat_detector.py` di modul. Guidance ada di CONTRIBUTING.md.

**Q: Bagaimana kontribusi?**
A: Baca CONTRIBUTING.md untuk semantic commit guidelines dan branch strategy.

---

## 🚀 YOU'RE READY!

Sekarang Anda sudah siap! 🎉

**Next actions:**
1. ✅ Setup project (Anda sudah di sini!)
2. 📖 Baca dokumentasi lebih detail
3. 🔍 Eksplor kode yang ada
4. 💬 Join komunitas / tanya pertanyaan
5. 🤝 Berkontribusi ke project

---

**Stuck? Ada pertanyaan?** 
- 💬 Buka [GitHub Issues](https://github.com/TEUNGKU-ZULKIFLI/TME-CORE/issues)
- 📧 Hubungi maintainer
- 🤖 Tanya ke AI Assistant Anda!

**Last Updated:** April 2026 | **For:** Beginners & First-Time Contributors
