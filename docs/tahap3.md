# TME-CORE: MikroTik Threat Mitigation Engine
> **Deskripsi**:
Sistem mitigasi otomatis serangan Brute Force SSH/FTP pada Router MikroTik dengan engine eksternal berbasis Python. Engine berjalan di server Debian dan menganalisa log secara real-time, mendeteksi anomali, dan melakukan blocking otomatis via API RouterOS dengan latency < 5 detik.

### 🧑‍💻 TAHAP: Mendeteksi Kegagalan Login
> **Deskripsi**:
Mendeteksi dengan cara memantau log berkala, serta membatasi jika kegagalan login mencapai `THRESHOLD` maka siap untuk dikirimkan ke`modul blokir`.

> [!WARNING]
> > **TAHAP Required: Tentunya Sudah Mengikuti TAHAP 1 &2 dong!**</br>
> > Clone pake **`SSH`**
> > ```bash
> > git clone git@github.com:TEUNGKU-ZULKIFLI/TME-CORE.git
> > ```
> > Atau memakai **`HTTPS`**
> > ```bash
> > git clone https://github.com/TEUNGKU-ZULKIFLI/TME-CORE.git
> > ```
> > Kemudian masuk kedirectory tersebut
> > ```bash
> > cd TME-CORE
> > ```
> > 
> > **TAHAP 2: Memulai fetching data log MikroTik**</br>
> > Pastinya dilingkungan **`Virtual Environment`**
> > ```bash
> > source venv/bin/activate
> > ```
> > Langsung Gas dengan Log ParserNya:
> > ```bash
> > python3 -m src.parser.log_parser
> > ```
> > Output Expect:
> > ```bash
> > (venv) user@user:~/TME-CORE$ python3 -m src.parser.log_parser
> > [+] SUKSES: Terhubung ke MikroTik xxx.xxx.xxx.1
> > 
> > [*] Mengambil raw data log dari API MikroTik...
> > [*] Jumlah total log di memory MikroTik saat ini: 221
> > 
> > === 5 RAW LOG TERAKHIR ===
> > {'id': '*D8', 'time': '07:54:04', 'topics': 'system,info,account', 'message': 'user admin logged in from xxx.xxx.xxx.2 via api'}
> > {'id': '*D9', 'time': '07:54:04', 'topics': 'system,info,account', 'message': 'user admin logged out from xxx.xxx.xxx.2 via api'}
> > {'id': '*DA', 'time': '07:58:24', 'topics': 'system,info,account', 'message': 'user admin logged in from xxx.xxx.xxx.2 via ssh'}
> > {'id': '*DB', 'time': '07:58:59', 'topics': 'system,info,account', 'message': 'user admin logged out from xxx.xxx.xxx.2 via ssh'}
> > {'id': '*DC', 'time': '08:34:52', 'topics': 'system,info,account', 'message': 'user admin logged in from xxx.xxx.xxx.2 via api'}
> > ==========================
> > 
> > [*] Koneksi ke MikroTik ditutup dengan aman.
> > (venv) user@user:~/TME-CORE$
> > ```
> > > [!TIP]
> > > Samakah Output dengan expect? kalau sama rayakan dengan teman sebelahmu itu 🫵🎉.

#### TAHAP 3.1: Mulai deteksi kegagalan login
Pastinya dilingkungan **`Virtual Environment`**
```bash
source venv/bin/activate
```
Langsung Gas dengan Detection:
```bash
python3 -m src.detection.detector_jalur_a
```
Output Expect:
```bash
(venv) user@user:~/TME-CORE$ python3 -m src.detection.detector_jalur_a
[+] SUKSES: Terhubung ke MikroTik xxx.xxx.xxx.1
[-] Memulai pemantauan log (Mode Verbose)...
[*] [DEBUG] Mengambil 11 log dari MikroTik...
[*] [DEBUG] Mengambil 11 log dari MikroTik...
[*] [DEBUG] Mengambil 11 log dari MikroTik...
[*] [DEBUG] Mengambil 11 log dari MikroTik...
```
Kemudian untuk menghentikan proses cukup **`Ctrl + c`**
```bash
^C
[*] Pemantauan dihentikan user.
[*] Koneksi ke MikroTik ditutup dengan aman.
(venv) user@user:~/TME-CORE$
```
#### TAHAP 3.2: Mulai mencoba login gagal
Pastinya sudah pernah mencoba **`remote SSH`**
```bash
ssh -o MACs=hmac-sha1 admin@xxx.xxx.xxx.1
```
Jangan lupa dengan menjalankan `detector_jalur_a`
```bash
python3 -m src.detection.detector_jalur_a
```
Pastikan untuk tidak keluar dulu dan memonitoring pada saat password remote **`SSH`** salah.</br>
Dengan dual terminal jadinya:</br>
Terminal **`Remote SSH`** serta mencoba dengan password yang salah:
```bash
root@user:/home/user# ssh -o MACs=hmac-sha1 admin@xxx.xxx.xxx.1
admin@xxx.xxx.xxx.1's password:
Permission denied, please try again.
admin@xxx.xxx.xxx.1's password:
Permission denied, please try again.
admin@xxx.xxx.xxx.1's password:
admin@xxx.xxx.xxx.1: Permission denied (password).
root@user:/home/user# ssh -o MACs=hmac-sha1 admin@xxx.xxx.xxx.1
admin@xxx.xxx.xxx.1's password:
Permission denied, please try again.
admin@xxx.xxx.xxx.1's password:
Permission denied, please try again.
admin@xxx.xxx.xxx.1's password:
admin@xxx.xxx.xxx.1: Permission denied (password).
root@user:/home/user# ssh -o MACs=hmac-sha1 admin@xxx.xxx.xxx.1
admin@xxx.xxx.xxx.1's password:
Permission denied, please try again.
admin@xxx.xxx.xxx.1's password:
Permission denied, please try again.
admin@xxx.xxx.xxx.1's password:
admin@xxx.xxx.xxx.1: Permission denied (password).
root@user:/home/user#
```
Terminal **`Detector Jalur A`** hasilnya:
```bash
(venv) user@user:~/TME-CORE$ python3 -m src.detection.detector_jalur_a
[+] SUKSES: Terhubung ke MikroTik xxx.xxx.xxx.1
[-] Memulai pemantauan log (Mode Verbose)...
[*] [DEBUG] Mengambil 13 log dari MikroTik...
[*] [DEBUG] Mengambil 13 log dari MikroTik...
[*] [DEBUG] Mengambil 14 log dari MikroTik...
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Total: 1x) | ID: *D
[*] [DEBUG] Mengambil 15 log dari MikroTik...
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Total: 2x) | ID: *E
[*] [DEBUG] Mengambil 16 log dari MikroTik...
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Total: 3x) | ID: *F
[*] [DEBUG] Mengambil 17 log dari MikroTik...
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Total: 4x) | ID: *10
[*] [DEBUG] Mengambil 19 log dari MikroTik...
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Total: 5x) | ID: *11
[>>>] THRESHOLD TERCAPAI: IP xxx.xxx.xxx.2 siap dikirim ke modul blokir!
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Total: 1x) | ID: *12
[#] AKSI JALUR A: Siapkan script pemblokiran untuk IP ['xxx.xxx.xxx.2']
[*] [DEBUG] Mengambil 19 log dari MikroTik...
[*] [DEBUG] Mengambil 22 log dari MikroTik...
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Total: 2x) | ID: *13
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Total: 3x) | ID: *14
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Total: 4x) | ID: *15
[*] [DEBUG] Mengambil 22 log dari MikroTik...
[*] [DEBUG] Mengambil 22 log dari MikroTik...
```
#### RANGKUMAN
Dari Output Monitoring `Detector Jalur A` kita mendapatkan info bahwa IP `xxx.xxx.xxx.2` Mencoba login tapi salah mulu passwordnya dengan menetapkan `THRESHOLD` maka siap untuk dikirimkan ke`modul blokir`.

### RECAP ALL:
> **`TAHAPAN 3.1:`**
> > ```bash
> > user@user:~/TME-CORE$ source venv/bin/activate
> > (venv) user@user:~/TME-CORE$ python3 -m src.detection.detector_jalur_a
> > [+] SUKSES: Terhubung ke MikroTik xxx.xxx.xxx.1
> > [-] Memulai pemantauan log (Mode Verbose)...
> > [*] [DEBUG] Mengambil 11 log dari MikroTik...
> > [*] [DEBUG] Mengambil 11 log dari MikroTik...
> > [*] [DEBUG] Mengambil 11 log dari MikroTik...
> > [*] [DEBUG] Mengambil 11 log dari MikroTik...
> > ^C
> > [*] Pemantauan dihentikan user.
> > [*] Koneksi ke MikroTik ditutup dengan aman.
> > (venv) user@user:~/TME-CORE$
> > ```

> **`TAHAPAN 3.2:`**
> > **`TAHAPAN 3.2.1:`**
> > ```bash
> > root@user:/home/user# ssh -o MACs=hmac-sha1 admin@xxx.xxx.xxx.1
> > admin@xxx.xxx.xxx.1's password:
> > Permission denied, please try again.
> > admin@xxx.xxx.xxx.1's password:
> > Permission denied, please try again.
> > admin@xxx.xxx.xxx.1's password:
> > admin@xxx.xxx.xxx.1: Permission denied (password).
> > root@user:/home/user# ssh -o MACs=hmac-sha1 admin@xxx.xxx.xxx.1
> > admin@xxx.xxx.xxx.1's password:
> > Permission denied, please try again.
> > admin@xxx.xxx.xxx.1's password:
> > Permission denied, please try again.
> > admin@xxx.xxx.xxx.1's password:
> > admin@xxx.xxx.xxx.1: Permission denied (password).
> > root@user:/home/user# ssh -o MACs=hmac-sha1 admin@xxx.xxx.xxx.1
> > admin@xxx.xxx.xxx.1's password:
> > Permission denied, please try again.
> > admin@xxx.xxx.xxx.1's password:
> > Permission denied, please try again.
> > admin@xxx.xxx.xxx.1's password:
> > admin@xxx.xxx.xxx.1: Permission denied (password).
> > root@user:/home/user#
> > ```
> > **`TAHAPAN 3.2.2:`**
> > ```bash
> > (venv) user@user:~/TME-CORE$ python3 -m src.detection.detector_jalur_a
> > [+] SUKSES: Terhubung ke MikroTik xxx.xxx.xxx.1
> > [-] Memulai pemantauan log (Mode Verbose)...
> > [*] [DEBUG] Mengambil 13 log dari MikroTik...
> > [*] [DEBUG] Mengambil 13 log dari MikroTik...
> > [*] [DEBUG] Mengambil 14 log dari MikroTik...
> > [!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Total: 1x) | ID: *D
> > [*] [DEBUG] Mengambil 15 log dari MikroTik...
> > [!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Total: 2x) | ID: *E
> > [*] [DEBUG] Mengambil 16 log dari MikroTik...
> > [!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Total: 3x) | ID: *F
> > [*] [DEBUG] Mengambil 17 log dari MikroTik...
> > [!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Total: 4x) | ID: *10
> > [*] [DEBUG] Mengambil 19 log dari MikroTik...
> > [!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Total: 5x) | ID: *11
> > [>>>] THRESHOLD TERCAPAI: IP xxx.xxx.xxx.2 siap dikirim ke modul blokir!
> > [!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Total: 1x) | ID: *12
> > [#] AKSI JALUR A: Siapkan script pemblokiran untuk IP ['xxx.xxx.xxx.2']
> > [*] [DEBUG] Mengambil 19 log dari MikroTik...
> > [*] [DEBUG] Mengambil 22 log dari MikroTik...
> > [!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Total: 2x) | ID: *13
> > [!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Total: 3x) | ID: *14
> > [!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Total: 4x) | ID: *15
> > [*] [DEBUG] Mengambil 22 log dari MikroTik...
> > [*] [DEBUG] Mengambil 22 log dari MikroTik...
> > ```
