# TME-CORE: MikroTik Threat Mitigation Engine
> **Deskripsi**:
Sistem mitigasi otomatis serangan Brute Force SSH/FTP pada Router MikroTik dengan engine eksternal berbasis Python. Engine berjalan di server Debian dan menganalisa log secara real-time, mendeteksi anomali, dan melakukan blocking otomatis via API RouterOS dengan latency < 5 detik.

### 🧑‍💻 TAHAP: Jalur A - Mendeteksi log Brute Force
> **Deskripsi**:
Mendeteksi dengan cara memantau log berkala, serta membatasi jika kegagalan login mencapai `THRESHOLD` maka siap untuk dikirimkan ke`modul blokir`.

> [!WARNING]
> > **`SUDAH MENGIKUTI TAHAPAN BERIKUT INI:`**</br>
> > **🧑‍💻 TAHAP: Jembatan komunikasi ke RouterOS**</br>
> > **Deskripsi**:</br>
> > *Membangun koneksi dasar!*</br>
> > **🧑‍💻 TAHAP: Pengecekan Raw Data Log MikroTik**</br>
> > **Deskripsi**:</br>
> > *Mengambil data log mikrotik dasar dengan 5 RAW LOG TERAKHIR!*</br>
> > *Pada Dasarnya sama seperti terminal mikrotik dengan `log print`*</br>

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
##### RANGKUMAN 3.1 - 3.2:
Dari Output Monitoring `Detector Jalur A` kita mendapatkan info bahwa IP `xxx.xxx.xxx.2` Mencoba login tapi salah mulu passwordnya dengan menetapkan `THRESHOLD` maka siap untuk dikirimkan ke`modul blokir`.

#### TAHAP 3.3: Update Jalur A - Eksekusi pemblokiran IP
Setup MikroTik:</br>
Menyiapkan sebuah penampung List IP Penyerang!
```bash
[admin@MikroTik] > ip firewall address-list add address=0.0.0.0/32 list=brute_force_block comment="Placeholder - auto-populated by TME-CORE"
```
Menyiapkan sebuah aturan firewall untuk memblokir serta memasukkan IP Penyerang ke penampung tadi!
```bash
[admin@MikroTik] > ip firewall filter add chain=input src-address-list=brute_force_block action=drop comment="Drop brute_force_block - TME-CORE"
```
> [!IMPORTANT]
> Jalankan ulang **`TAHAP 3.1 s/d 3.2`** dan memastikan IP Tersebut berhasil diblokir!

#### TAHAP 3.4:
Pastinya dilingkungan **`Virtual Environment`**
```bash
source venv/bin/activate
```
Langsung Gas dengan Detection:
```bash
python3 -m src.detection.detector_jalur_a
```
Output expect:
```bash
(venv) user@user:~/TME-CORE$ python3 -m src.detection.detector_jalur_a
[+] SUKSES: Terhubung ke MikroTik xxx.xxx.xxx.1
[-] TME-CORE (JALUR A) AKTIF: Menunggu serangan masuk...
[*] Memori disiapkan. Mengabaikan 28 log lama.
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-1)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-2)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-3)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-4)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-5)
[>>>] THRESHOLD TERCAPAI: Melakukan pemblokiran pada xxx.xxx.xxx.2!
[*] MITIGASI: IP xxx.xxx.xxx.2 sudah berstatus TERBLOKIR sebelumnya.
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-1)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-2)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-3)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-4)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-5)
[>>>] THRESHOLD TERCAPAI: Melakukan pemblokiran pada xxx.xxx.xxx.2!
[*] MITIGASI: IP xxx.xxx.xxx.2 sudah berstatus TERBLOKIR sebelumnya.
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-1)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-2)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-3)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-4)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-5)
[>>>] THRESHOLD TERCAPAI: Melakukan pemblokiran pada xxx.xxx.xxx.2!
[*] MITIGASI: IP xxx.xxx.xxx.2 sudah berstatus TERBLOKIR sebelumnya.
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-1)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-2)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-3)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-4)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-5)
[>>>] THRESHOLD TERCAPAI: Melakukan pemblokiran pada xxx.xxx.xxx.2!
[*] MITIGASI: IP xxx.xxx.xxx.2 sudah berstatus TERBLOKIR sebelumnya.
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-1)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-2)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-3)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-4)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-5)
[>>>] THRESHOLD TERCAPAI: Melakukan pemblokiran pada xxx.xxx.xxx.2!
[*] MITIGASI: IP xxx.xxx.xxx.2 sudah berstatus TERBLOKIR sebelumnya.
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-1)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-2)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-3)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-4)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-5)
[>>>] THRESHOLD TERCAPAI: Melakukan pemblokiran pada xxx.xxx.xxx.2!
[*] MITIGASI: IP xxx.xxx.xxx.2 sudah berstatus TERBLOKIR sebelumnya.
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-1)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-2)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-3)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-4)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-5)
[>>>] THRESHOLD TERCAPAI: Melakukan pemblokiran pada xxx.xxx.xxx.2!
[*] MITIGASI: IP xxx.xxx.xxx.2 sudah berstatus TERBLOKIR sebelumnya.
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-1)
```
Kemudian close dengan mengetik **`Ctrl + c`**:
```bash
^C
[*] Pemantauan dihentikan user.
[*] Koneksi ke MikroTik ditutup dengan aman.
(venv) user@user:~/TME-CORE$
```
Validasi dengan login ke MikroTik dan cek:
```bash
[admin@MikroTik] > ip firewall address-list print
```
Output expect:
```bash
Flags: X - disabled, D - dynamic
 #   LIST             					            ADDRESS		    CREATION-TIME        TIMEOUT
 0   ;;; Placeholder - auto-populated by TME-CORE
     brute_force_block 					            0.0.0.0		    may/08/2026 02:08:32
 1 D ;;; Auto-blocked by TME-CORE
     brute_force_block 					            xxx.xxx.xxx.2	may/16/2026 01:56:55 50m40s
```
> [!TIP]
> **Untuk menghapus IP tersebut dari list `IP Peretas` dengan**:</br>
> ```bash
> [admin@MikroTik] > ip firewall address-list remove numbers=1
> ```
> **Lalu cek Kembali dengan**:</br>
> ```bash
> [admin@MikroTik] > ip firewall address-list print
> ```

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