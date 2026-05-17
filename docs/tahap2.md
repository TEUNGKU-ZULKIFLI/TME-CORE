# TME-CORE: MikroTik Threat Mitigation Engine
> **Deskripsi**:
Sistem mitigasi otomatis serangan Brute Force SSH/FTP pada Router MikroTik dengan engine eksternal berbasis Python. Engine berjalan di server Debian dan menganalisa log secara real-time, mendeteksi anomali, dan melakukan blocking otomatis via API RouterOS dengan latency < 5 detik.

### 🧑‍💻 TAHAP: Pengecekan Raw Data Log MikroTik
> **Deskripsi**:
Mengambil data log mikrotik dasar dengan 5 RAW LOG TERAKHIR!</br>
Pada Dasarnya sama seperti terminal mikrotik dengan `log print`

> [!WARNING]
> > **`SUDAH MENGIKUTI TAHAPAN BERIKUT INI:`**</br>
> > **🧑‍💻 TAHAP: Jembatan komunikasi ke RouterOS**</br>
> > **Deskripsi**:</br>
> > *Membangun koneksi dasar!*</br>

#### TAHAP 2: Memulai fetching data log MikroTik
Pastinya dilingkungan **`Virtual Environment`**
```bash
source venv/bin/activate
```
Langsung Gas dengan Log ParserNya:
```bash
python3 -m src.parser.log_parser
```
Output Expect:
```bash
(venv) user@user:~/TME-CORE$ python3 -m src.parser.log_parser
[+] SUKSES: Terhubung ke MikroTik xxx.xxx.xxx.1

[*] Mengambil raw data log dari API MikroTik...
[*] Jumlah total log di memory MikroTik saat ini: 221

=== 5 RAW LOG TERAKHIR ===
{'id': '*D8', 'time': '07:54:04', 'topics': 'system,info,account', 'message': 'user admin logged in from xxx.xxx.xxx.2 via api'}
{'id': '*D9', 'time': '07:54:04', 'topics': 'system,info,account', 'message': 'user admin logged out from xxx.xxx.xxx.2 via api'}
{'id': '*DA', 'time': '07:58:24', 'topics': 'system,info,account', 'message': 'user admin logged in from xxx.xxx.xxx.2 via ssh'}
{'id': '*DB', 'time': '07:58:59', 'topics': 'system,info,account', 'message': 'user admin logged out from xxx.xxx.xxx.2 via ssh'}
{'id': '*DC', 'time': '08:34:52', 'topics': 'system,info,account', 'message': 'user admin logged in from xxx.xxx.xxx.2 via api'}
==========================

[*] Koneksi ke MikroTik ditutup dengan aman.
(venv) user@user:~/TME-CORE$
```
> [!TIP]
> Samakah Output dengan expect? kalau sama rayakan dengan teman sebelahmu itu 🫵🎉.

### RECAP ALL:
```bash
user@user:~/TME-CORE$ source venv/bin/activate
(venv) user@user:~/TME-CORE$ python3 -m src.parser.log_parser
[+] SUKSES: Terhubung ke MikroTik xxx.xxx.xxx.1

[*] Mengambil raw data log dari API MikroTik...
[*] Jumlah total log di memory MikroTik saat ini: 221

=== 5 RAW LOG TERAKHIR ===
{'id': '*D8', 'time': '07:54:04', 'topics': 'system,info,account', 'message': 'user admin logged in from xxx.xxx.xxx.2 via api'}
{'id': '*D9', 'time': '07:54:04', 'topics': 'system,info,account', 'message': 'user admin logged out from xxx.xxx.xxx.2 via api'}
{'id': '*DA', 'time': '07:58:24', 'topics': 'system,info,account', 'message': 'user admin logged in from xxx.xxx.xxx.2 via ssh'}
{'id': '*DB', 'time': '07:58:59', 'topics': 'system,info,account', 'message': 'user admin logged out from xxx.xxx.xxx.2 via ssh'}
{'id': '*DC', 'time': '08:34:52', 'topics': 'system,info,account', 'message': 'user admin logged in from xxx.xxx.xxx.2 via api'}
==========================

[*] Koneksi ke MikroTik ditutup dengan aman.
(venv) user@user:~/TME-CORE$
```
