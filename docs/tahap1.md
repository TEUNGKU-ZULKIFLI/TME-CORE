<p align="center">
  <picture>
    <source media="(prefers-color-scheme: night)" srcset="../assets/logos/TME-logo01.png" />
    <img src="../assets/logos/TME-logo01.png" width="500" />
  </picture>
</p>
<h1 align="center">
  <span><b align="center">🧑‍💻 TAHAP: Jembatan komunikasi ke RouterOS</b></span>
</h1>

**Deskripsi**:</br>
Membangun koneksi dasar!

#### TAHAP 1.1: Clone Repository ini
Clone pake **`SSH`**
```bash
git clone git@github.com:TEUNGKU-ZULKIFLI/TME-CORE.git
```
Atau memakai **`HTTPS`**
```bash
git clone https://github.com/TEUNGKU-ZULKIFLI/TME-CORE.git
```
Kemudian masuk kedirectory tersebut
```bash
cd TME-CORE
```

#### TAHAP 1.2: Konfigurasi file Config `config/config.py.example`
```bash
cp config/config.py.example config/config.py
```
Dan mulai mengonfigurasi dengan sesuai seperti:
```config
# 1. Kredensial MikroTik (RouterBoard)
MIKROTIK_IP = "xxx.xxx.xxx.1"  # IP RouterBoard yang bisa ping dari server yang cloning repo ini!
MIKROTIK_USER = "admin"       # username RouterBoard dapat disesuaikan
MIKROTIK_PASS = "*****"       # password RouterBoard
MIKROTIK_PORT = 8728          # Default port API MikroTik (Gunakan 8729 untuk API-SSL jika aktif)
```
Yang lainnya default aja dulu karena ini `Membangun koneksi dasar`Nya dulu.

#### TAHAP 1.3: Running First
Pastikan dilingkungan **`Virtual Environment`**
```bash
pyton3 -m venv venv
```
Aktifkan lingkungan **`Virtual Environment`**
```bash
source venv/bin/activate
```
Memastikannya cukup melihat terminal yang dimulai dengan `(venv) user@user:~/TME-CORE$`</br>
Upgrade pip dulu
```bash
pip install --upgrade pip
```
Menginstall reqirements yang dibutuhkan
```bash
pip install -r requirements.txt
```
Melihat package sudah terinstall
```bash
pip list
```

#### TAHAP 1.4: Engine Start
```bash
python3 -m src.api.connection
```
Ouput expect:
```bash
(venv) user@user:~/TME-CORE$ python3 -m src.api.connection
Mencoba koneksi ke MikroTik...
[+] SUKSES: Terhubung ke MikroTik xxx.xxx.xxx.1
[*] Koneksi ke MikroTik ditutup dengan aman.
(venv) user@user:~/TME-CORE$
```
> [!TIP]
> Kalau Output samaan Rayakan dengan teman sebelah anda 🫵🎉.

#### TAHAP 1.5: Validasi Connection
Memastikan diMikroTik dengan:
```bash
[admin@MikroTik] > log print
```
Output Expect:
```bash
07:54:04 system,info,account user admin logged in from xxx.xxx.xxx.2 via api
07:54:04 system,info,account user admin logged out from xxx.xxx.xxx.2 via api
```

### RECAP ALL:
```bash
user@user:~/TME-CORE$ python3 -m venv venv
user@user:~/TME-CORE$ source venv/bin/activate
(venv) user@user:~/TME-CORE$ pip install --upgrade pip
Requirement already satisfied: pip in ./venv/lib/python3.11/site-packages (23.0.1)
Collecting pip
  Using cached pip-26.1.1-py3-none-any.whl (1.8 MB)
Installing collected packages: pip
  Attempting uninstall: pip
    Found existing installation: pip 23.0.1
    Uninstalling pip-23.0.1:
      Successfully uninstalled pip-23.0.1
Successfully installed pip-26.1.1
(venv) user@user:~/TME-CORE$ pip install -r requirements.txt
Collecting routeros-api==0.21.0 (from -r requirements.txt (line 1))
  Using cached routeros_api-0.21.0-py2.py3-none-any.whl.metadata (10 kB)
Using cached routeros_api-0.21.0-py2.py3-none-any.whl (22 kB)
Installing collected packages: routeros-api
Successfully installed routeros-api-0.21.0
(venv) user@user:~/TME-CORE$ pip list
Package      Version
------------ -------
pip          26.1.1
RouterOS-api 0.21.0
setuptools   66.1.1
(venv) user@user:~/TME-CORE$ python3 -m src.api.connection
Mencoba koneksi ke MikroTik...
[+] SUKSES: Terhubung ke MikroTik xxx.xxx.xxx.1
[*] Koneksi ke MikroTik ditutup dengan aman.
(venv) user@user:~/TME-CORE$
```
<p align=right>
<a href="./all-tahap.md#--teungku-mitigation-engine---core">
  <img src="https://img.shields.io/badge/🏁-MAIN-red?style=for-the-badge" />
</a>
<a href="./tahap2.md#--%E2%80%8D-tahap-pengecekan-raw-data-log-mikrotik">
  <img src="https://img.shields.io/badge/🔜-SOON-green?style=for-the-badge" />
</a>
</p>