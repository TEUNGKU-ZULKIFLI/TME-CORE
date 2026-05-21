<p align="center">
  <picture>
    <source media="(prefers-color-scheme: night)" srcset="../assets/logos/TME-logo01.png" />
    <img src="../assets/logos/TME-logo01.png" width="500" />
  </picture>
</p>
<h1 align="center">
  <span><b align="center">🧑‍💻 TAHAP: Jalur B - Menganalisa Beban Router (CPU Monitor)</b></span>
</h1>

**Deskripsi**:</br>
Memonitoring secara berkala **`CPU & Memory`** Router.

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

#### TAHAP 4: Mulai monitoring CPU & MEMORY
Pastinya dilingkungan **`Virtual Environment`**
```bash
source venv/bin/activate
```
Langsung Gas dengan Monitoring:
```bash
python3 -m src.monitoring.evaluator_jalur_b
```
Output Expect:
```bash
(venv) user@user:~/TME-CORE$ python3 -m src.monitoring.evaluator_jalur_b
[+] SUKSES: Terhubung ke MikroTik xxx.xxx.xxx.1
[-] TME-CORE (JALUR B) AKTIF: Memonitor Beban Router...
[*] BEBAN ROUTER -> CPU: 0% | RAM: 71%
[*] BEBAN ROUTER -> CPU: 0% | RAM: 71%
[*] BEBAN ROUTER -> CPU: 0% | RAM: 71%
[*] BEBAN ROUTER -> CPU: 25% | RAM: 71%
[*] BEBAN ROUTER -> CPU: 0% | RAM: 71%
[*] BEBAN ROUTER -> CPU: 25% | RAM: 71%
[*] BEBAN ROUTER -> CPU: 0% | RAM: 71%
[*] BEBAN ROUTER -> CPU: 0% | RAM: 71%
[*] BEBAN ROUTER -> CPU: 0% | RAM: 71%
```
Kemudian close untuk monitoring **`CPU & RAM`** cukup ketik **`Ctrl + c`**:
```bash
^C
[*] Pemantauan dihentikan user.
[*] Koneksi ke MikroTik ditutup dengan aman.
(venv) user@user:~/TME-CORE$ 
```

### RECAP ALL:
```bash
user@user:~/TME-CORE$ source venv/bin/activate
(venv) user@user:~/TME-CORE$ python3 -m src.monitoring.evaluator_jalur_b
[+] SUKSES: Terhubung ke MikroTik xxx.xxx.xxx.1
[-] TME-CORE (JALUR B) AKTIF: Memonitor Beban Router...
[*] BEBAN ROUTER -> CPU: 0% | RAM: 71%
[*] BEBAN ROUTER -> CPU: 0% | RAM: 71%
[*] BEBAN ROUTER -> CPU: 0% | RAM: 71%
[*] BEBAN ROUTER -> CPU: 25% | RAM: 71%
[*] BEBAN ROUTER -> CPU: 0% | RAM: 71%
[*] BEBAN ROUTER -> CPU: 25% | RAM: 71%
[*] BEBAN ROUTER -> CPU: 0% | RAM: 71%
[*] BEBAN ROUTER -> CPU: 0% | RAM: 71%
[*] BEBAN ROUTER -> CPU: 0% | RAM: 71%
^C
[*] Pemantauan dihentikan user.
[*] Koneksi ke MikroTik ditutup dengan aman.
(venv) user@user:~/TME-CORE$ 
```
<p align=right>
<a href="./tahap3.md#--%E2%80%8D-tahap-jalur-a---mendeteksi-log-brute-force">
  <img src="https://img.shields.io/badge/🔙-BACK-red?style=for-the-badge" />
</a>
<a href="./tahap5.md#--%E2%80%8D-tahap-menggabungkan-jalur-a-deteksi--jalur-b-evaluasi-kinerja">
  <img src="https://img.shields.io/badge/🔜-SOON-green?style=for-the-badge" />
</a>
</p>