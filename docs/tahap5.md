# TME-CORE: MikroTik Threat Mitigation Engine
> **Deskripsi**:</br>
Sistem mitigasi otomatis serangan Brute Force SSH/FTP pada Router MikroTik dengan engine eksternal berbasis Python. Engine berjalan di server Debian dan menganalisa log secara real-time, mendeteksi anomali, dan melakukan blocking otomatis via API RouterOS dengan latency < 5 detik.

### 🧑‍💻 TAHAP: Menggabungkan Jalur A (Deteksi) & Jalur B (Evaluasi Kinerja)
> **Deskripsi**:</br>
Membaca **`/log (Jalur A)`**. Hanya jika ada indikasi `Brute Force`, baru membaca **`/system/resource (Jalur B)`** untuk merekam beban CPU saat itu, mencatatnya ke **`file log`**.

> [!WARNING]
> > **`SUDAH MENGIKUTI TAHAPAN BERIKUT INI:`**</br>
> > **🧑‍💻 TAHAP: Jembatan komunikasi ke RouterOS**</br>
> > **Deskripsi**:</br>
> > *Membangun koneksi dasar!*</br>
> > **🧑‍💻 TAHAP: Pengecekan Raw Data Log MikroTik**</br>
> > **Deskripsi**:</br>
> > *Mengambil data log mikrotik dasar dengan 5 RAW LOG TERAKHIR!*</br>
> > *Pada Dasarnya sama seperti terminal mikrotik dengan `log print`*</br>
> > **🧑‍💻 TAHAP: Jalur A - Mendeteksi log Brute Force**</br>
> > **Deskripsi**:</br>
> > *Mendeteksi dengan cara memantau log berkala, serta membatasi jika kegagalan login mencapai `THRESHOLD` maka siap untuk dikirimkan ke`modul blokir`.*</br>
> > **🧑‍💻 TAHAP: Jalur B - Menganalisa Beban Router (CPU Monitor)**</br>
> > **Deskripsi**:</br>
> > *Memonitoring secara berkala **`CPU & Memory`** Router.*</br>

#### TAHAP 5: Mulai Running Engine
Pastinya dilingkungan **`Virtual Environment`**
```bash
source venv/bin/activate
```
Langsung Gas dengan Running Engine:
```bash
python3 -m src.main_engine
```
Output expect:
```bash
(venv) user@user:~/TME-CORE$ python3 -m src.main_engine
[+] SUKSES: Terhubung ke MikroTik xxx.xxx.xxx.1
==================================================
[-] TME-CORE AKTIF: Deteksi (Jalur A) & Evaluasi (Jalur B)
==================================================
[*] Memori disiapkan. Mengabaikan 86 log lama.
```
Dan dilanjutkan dengan melakukan login remote **`SSH`** Router Mikrotik</br>
tentunya dengan password yang salah, serta menyepam untuk melihat pemblokiran ini berhasil.
```bash
ssh -o MACs=hmac-sha1 admin@xxx.xxx.xxx.1
```
Output expect:
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
Kembali keEngine yang sedang Running dan lihat</br>
Output expect:
```bash
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-1)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-2)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-3)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-4)
[*] DATA EVALUASI DISIMPAN: CPU 100% | RAM sisa 8.58MB
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-5)
[>>>] THRESHOLD TERCAPAI: Melakukan pemblokiran pada xxx.xxx.xxx.2!
[!] MITIGASI: Mengeksekusi pemblokiran untuk IP xxx.xxx.xxx.2...
[+] SUKSES: IP xxx.xxx.xxx.2 berhasil dimasukkan ke Address List 'brute_force_block'
[*] DATA EVALUASI DISIMPAN: CPU 100% | RAM sisa 8.58MB
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-1)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-2)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-3)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-4)
[*] DATA EVALUASI DISIMPAN: CPU 100% | RAM sisa 8.58MB
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-5)
[>>>] THRESHOLD TERCAPAI: Melakukan pemblokiran pada xxx.xxx.xxx.2!
[*] MITIGASI: IP xxx.xxx.xxx.2 sudah berstatus TERBLOKIR sebelumnya.
[*] DATA EVALUASI DISIMPAN: CPU 100% | RAM sisa 8.58MB
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-1)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-2)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-3)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-4)
[*] DATA EVALUASI DISIMPAN: CPU 100% | RAM sisa 8.58MB
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-5)
[>>>] THRESHOLD TERCAPAI: Melakukan pemblokiran pada xxx.xxx.xxx.2!
[*] MITIGASI: IP xxx.xxx.xxx.2 sudah berstatus TERBLOKIR sebelumnya.
[*] DATA EVALUASI DISIMPAN: CPU 100% | RAM sisa 8.58MB
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-1)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-2)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-3)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-4)
[*] DATA EVALUASI DISIMPAN: CPU 100% | RAM sisa 8.58MB
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-5)
[>>>] THRESHOLD TERCAPAI: Melakukan pemblokiran pada xxx.xxx.xxx.2!
[*] MITIGASI: IP xxx.xxx.xxx.2 sudah berstatus TERBLOKIR sebelumnya.
[*] DATA EVALUASI DISIMPAN: CPU 100% | RAM sisa 8.58MB
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-1)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-2)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-3)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-4)
[*] DATA EVALUASI DISIMPAN: CPU 100% | RAM sisa 8.58MB
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-5)
[>>>] THRESHOLD TERCAPAI: Melakukan pemblokiran pada xxx.xxx.xxx.2!
[*] MITIGASI: IP xxx.xxx.xxx.2 sudah berstatus TERBLOKIR sebelumnya.
[*] DATA EVALUASI DISIMPAN: CPU 100% | RAM sisa 8.58MB
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-1)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-2)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-3)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-4)
[*] DATA EVALUASI DISIMPAN: CPU 100% | RAM sisa 8.58MB
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-5)
[>>>] THRESHOLD TERCAPAI: Melakukan pemblokiran pada xxx.xxx.xxx.2!
[*] MITIGASI: IP xxx.xxx.xxx.2 sudah berstatus TERBLOKIR sebelumnya.
[*] DATA EVALUASI DISIMPAN: CPU 100% | RAM sisa 8.58MB
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-1)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-2)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-3)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-4)
[*] DATA EVALUASI DISIMPAN: CPU 100% | RAM sisa 8.58MB
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-5)
[>>>] THRESHOLD TERCAPAI: Melakukan pemblokiran pada xxx.xxx.xxx.2!
[*] MITIGASI: IP xxx.xxx.xxx.2 sudah berstatus TERBLOKIR sebelumnya.
[*] DATA EVALUASI DISIMPAN: CPU 100% | RAM sisa 8.58MB
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-1)
```
Kemudian closing engine cukup ketik **`Ctrl + c`**:
```bash
^C
[*] Pemantauan dihentikan user.
[*] Koneksi ke MikroTik ditutup dengan aman.
(venv) user@user:~/TME-CORE$
```
Setelah closing engine, pada folder root `~/TME-CORE` akan ada file **`tmecore.log`**</br>
Mari kita intip file log tersebut dengan:
```bash
tail -f tmecore.log
```
Output expect:
```bash
(venv) user@user:~/TME-CORE$ tail -f tmecore.log
[2026-05-17 23:45:42] IP: xxx.xxx.xxx.2 | Aksi: SEDANG DISERANG | CPU: 100% | Sisa RAM: 8.58MB / 32.00MB
[2026-05-17 23:45:42] IP: xxx.xxx.xxx.2 | Aksi: BERHASIL DIBLOKIR | CPU: 100% | Sisa RAM: 8.58MB / 32.00MB
[2026-05-17 23:45:42] IP: xxx.xxx.xxx.2 | Aksi: SEDANG DISERANG | CPU: 100% | Sisa RAM: 8.58MB / 32.00MB
[2026-05-17 23:45:42] IP: xxx.xxx.xxx.2 | Aksi: BERHASIL DIBLOKIR | CPU: 100% | Sisa RAM: 8.58MB / 32.00MB
[2026-05-17 23:45:42] IP: xxx.xxx.xxx.2 | Aksi: SEDANG DISERANG | CPU: 100% | Sisa RAM: 8.58MB / 32.00MB
[2026-05-17 23:45:42] IP: xxx.xxx.xxx.2 | Aksi: BERHASIL DIBLOKIR | CPU: 100% | Sisa RAM: 8.58MB / 32.00MB
[2026-05-17 23:45:42] IP: xxx.xxx.xxx.2 | Aksi: SEDANG DISERANG | CPU: 100% | Sisa RAM: 8.58MB / 32.00MB
[2026-05-17 23:45:42] IP: xxx.xxx.xxx.2 | Aksi: BERHASIL DIBLOKIR | CPU: 100% | Sisa RAM: 8.58MB / 32.00MB
[2026-05-17 23:45:42] IP: xxx.xxx.xxx.2 | Aksi: SEDANG DISERANG | CPU: 100% | Sisa RAM: 8.58MB / 32.00MB
[2026-05-17 23:45:42] IP: xxx.xxx.xxx.2 | Aksi: BERHASIL DIBLOKIR | CPU: 100% | Sisa RAM: 8.58MB / 32.00MB
```
Kemudian closing Intipan LOG cukup ketik **`Ctrl + c`**:
```bash
^C
(venv) user@user:~/TME-CORE$
```
Serta kevalidasian data dengan mengecek pada Router itu sendiri dengan:
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
```bash
user@user:~/TME-CORE$ source venv/bin/activate
(venv) user@user:~/TME-CORE$ python3 -m src.main_engine
[+] SUKSES: Terhubung ke MikroTik xxx.xxx.xxx.1
==================================================
[-] TME-CORE AKTIF: Deteksi (Jalur A) & Evaluasi (Jalur B)
==================================================
[*] Memori disiapkan. Mengabaikan 86 log lama.
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-1)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-2)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-3)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-4)
[*] DATA EVALUASI DISIMPAN: CPU 100% | RAM sisa 8.58MB
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-5)
[>>>] THRESHOLD TERCAPAI: Melakukan pemblokiran pada xxx.xxx.xxx.2!
[!] MITIGASI: Mengeksekusi pemblokiran untuk IP xxx.xxx.xxx.2...
[+] SUKSES: IP xxx.xxx.xxx.2 berhasil dimasukkan ke Address List 'brute_force_block'
[*] DATA EVALUASI DISIMPAN: CPU 100% | RAM sisa 8.58MB
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-1)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-2)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-3)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-4)
[*] DATA EVALUASI DISIMPAN: CPU 100% | RAM sisa 8.58MB
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-5)
[>>>] THRESHOLD TERCAPAI: Melakukan pemblokiran pada xxx.xxx.xxx.2!
[*] MITIGASI: IP xxx.xxx.xxx.2 sudah berstatus TERBLOKIR sebelumnya.
[*] DATA EVALUASI DISIMPAN: CPU 100% | RAM sisa 8.58MB
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-1)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-2)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-3)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-4)
[*] DATA EVALUASI DISIMPAN: CPU 100% | RAM sisa 8.58MB
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-5)
[>>>] THRESHOLD TERCAPAI: Melakukan pemblokiran pada xxx.xxx.xxx.2!
[*] MITIGASI: IP xxx.xxx.xxx.2 sudah berstatus TERBLOKIR sebelumnya.
[*] DATA EVALUASI DISIMPAN: CPU 100% | RAM sisa 8.58MB
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-1)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-2)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-3)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-4)
[*] DATA EVALUASI DISIMPAN: CPU 100% | RAM sisa 8.58MB
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-5)
[>>>] THRESHOLD TERCAPAI: Melakukan pemblokiran pada xxx.xxx.xxx.2!
[*] MITIGASI: IP xxx.xxx.xxx.2 sudah berstatus TERBLOKIR sebelumnya.
[*] DATA EVALUASI DISIMPAN: CPU 100% | RAM sisa 8.58MB
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-1)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-2)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-3)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-4)
[*] DATA EVALUASI DISIMPAN: CPU 100% | RAM sisa 8.58MB
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-5)
[>>>] THRESHOLD TERCAPAI: Melakukan pemblokiran pada xxx.xxx.xxx.2!
[*] MITIGASI: IP xxx.xxx.xxx.2 sudah berstatus TERBLOKIR sebelumnya.
[*] DATA EVALUASI DISIMPAN: CPU 100% | RAM sisa 8.58MB
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-1)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-2)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-3)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-4)
[*] DATA EVALUASI DISIMPAN: CPU 100% | RAM sisa 8.58MB
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-5)
[>>>] THRESHOLD TERCAPAI: Melakukan pemblokiran pada xxx.xxx.xxx.2!
[*] MITIGASI: IP xxx.xxx.xxx.2 sudah berstatus TERBLOKIR sebelumnya.
[*] DATA EVALUASI DISIMPAN: CPU 100% | RAM sisa 8.58MB
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-1)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-2)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-3)
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-4)
[*] DATA EVALUASI DISIMPAN: CPU 100% | RAM sisa 8.58MB
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-5)
[>>>] THRESHOLD TERCAPAI: Melakukan pemblokiran pada xxx.xxx.xxx.2!
[*] MITIGASI: IP xxx.xxx.xxx.2 sudah berstatus TERBLOKIR sebelumnya.
[*] DATA EVALUASI DISIMPAN: CPU 100% | RAM sisa 8.58MB
[!] DETEKSI: Gagal login dari xxx.xxx.xxx.2 (Gagal ke-1)
^C
[*] Pemantauan dihentikan user.
[*] Koneksi ke MikroTik ditutup dengan aman.
(venv) user@user:~/TME-CORE$ tail -f tmecore.log
[2026-05-17 23:45:42] IP: xxx.xxx.xxx.2 | Aksi: SEDANG DISERANG | CPU: 100% | Sisa RAM: 8.58MB / 32.00MB
[2026-05-17 23:45:42] IP: xxx.xxx.xxx.2 | Aksi: BERHASIL DIBLOKIR | CPU: 100% | Sisa RAM: 8.58MB / 32.00MB
[2026-05-17 23:45:42] IP: xxx.xxx.xxx.2 | Aksi: SEDANG DISERANG | CPU: 100% | Sisa RAM: 8.58MB / 32.00MB
[2026-05-17 23:45:42] IP: xxx.xxx.xxx.2 | Aksi: BERHASIL DIBLOKIR | CPU: 100% | Sisa RAM: 8.58MB / 32.00MB
[2026-05-17 23:45:42] IP: xxx.xxx.xxx.2 | Aksi: SEDANG DISERANG | CPU: 100% | Sisa RAM: 8.58MB / 32.00MB
[2026-05-17 23:45:42] IP: xxx.xxx.xxx.2 | Aksi: BERHASIL DIBLOKIR | CPU: 100% | Sisa RAM: 8.58MB / 32.00MB
[2026-05-17 23:45:42] IP: xxx.xxx.xxx.2 | Aksi: SEDANG DISERANG | CPU: 100% | Sisa RAM: 8.58MB / 32.00MB
[2026-05-17 23:45:42] IP: xxx.xxx.xxx.2 | Aksi: BERHASIL DIBLOKIR | CPU: 100% | Sisa RAM: 8.58MB / 32.00MB
[2026-05-17 23:45:42] IP: xxx.xxx.xxx.2 | Aksi: SEDANG DISERANG | CPU: 100% | Sisa RAM: 8.58MB / 32.00MB
[2026-05-17 23:45:42] IP: xxx.xxx.xxx.2 | Aksi: BERHASIL DIBLOKIR | CPU: 100% | Sisa RAM: 8.58MB / 32.00MB
^C
(venv) user@user:~/TME-CORE$
```