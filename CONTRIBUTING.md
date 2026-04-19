# Panduan Kontribusi TME-CORE

Terima kasih telah berkontribusi pada **TME-CORE (Traffic Mitigation External Core)**. Dokumen ini memastikan setiap perubahan terdokumentasi secara profesional melalui *Semantic Commits*.

---

## 🏗️ Format Pesan Commit

Gunakan formula berikut untuk menjaga riwayat proyek tetap bersih:

` <type>(<scope>): <emoji> <subject> `

Untuk memberikan detail lebih lanjut, gunakan beberapa flag `-m` di terminal:
` git commit -m "Header (Ringkasan)" -m "Body (Detail perubahan)" -m "Footer (Referensi Issue)" `

### 1. Daftar Type Commit
| Type | Emoji | Kegunaan |
| :--- | :---: | :--- |
| **feat** | ✨ | Fitur baru (logika mitigasi, modul baru) |
| **fix** | 🐛 | Perbaikan bug atau kesalahan logika |
| **docs** | 📝 | Dokumentasi (README, komentar kode, manual) |
| **style** | 🎨 | Perapian kode (formatting, PEP 8) tanpa ubah logika |
| **refactor** | ♻️ | Restrukturisasi kode agar lebih efisien |
| **test** | ✅ | Penambahan skenario uji atau validasi |
| **chore** | 🔧 | Tugas rutin (update library, config, .gitignore) |

### 2. Daftar Scope (Fase NDLC)
Gunakan *scope* untuk memperjelas fase pengembangan:
- **analysis**: Identifikasi pola log, threshold, dan metrik.
- **design**: Arsitektur engine, diagram topologi, dan flowchart.
- **simulation**: Lingkungan virtual, instalasi CHR, API dasar.
- **implementation**: Pengodean Python, integrasi MikroTik & Telegram.
- **monitoring**: Pengujian serangan (A/B Testing) & data real-time.
- **management**: Evaluasi hasil, laporan teknis, dan optimasi.

### 3. Branch Naming Convention
Gunakan nama branch yang konsisten agar mudah dilacak:
- `feat/<nama-fitur>` untuk fitur baru
- `fix/<nama-bug>` untuk perbaikan
- `docs/<nama-dokumen>` untuk dokumentasi
- `chore/<nama-tugas>` untuk tugas rutin atau cleanup

Contoh:
- `feat/analysis-baseline`
- `docs/measurement-protocol`
- `chore/gitignore-cleanup`

### 4. Aturan Kerja Sebelum Commit
Sebelum commit, cek poin berikut:
1. Pastikan file `.env` tidak ikut masuk commit.
2. Pastikan data eksperimen raw besar tidak langsung dipush jika belum disepakati.
3. Pastikan issue terkait sudah disebut di footer commit.
4. Pastikan perubahan satu tujuan per commit.
5. Jalankan review singkat pada README, docs, atau skrip yang diubah.

### 5. Flow Kerja yang Disarankan
1. Ambil issue yang ingin dikerjakan.
2. Buat branch baru sesuai scope.
3. Update dokumen atau kode.
4. Jalankan validasi lokal.
5. Commit dengan semantic commit.
6. Push branch, lalu buka Pull Request.

### 6. Struktur Commit yang Baik untuk Project Ini
Urutan yang umum dipakai:
- `docs(...)` untuk analisis, protokol, dan penjelasan
- `feat(...)` untuk kode utama
- `test(...)` untuk validasi dan pengujian
- `chore(...)` untuk cleanup, gitignore, dan struktur repo

---

## 💡 Contoh Commit dengan Detail (Multi-line)

Jika ingin menjelaskan perubahan secara mendalam, gunakan format ini:

```bash
git commit -m "feat(implementation): ✨ tambah modul ekstraksi log via api" \
           -m "Menambahkan fungsi parsing log MikroTik menggunakan port 8728 untuk mempercepat deteksi." \
           -m "Closes #4"
```

---

## ⚠️ Catatan Penting
- **Imperative Mood**: Gunakan kata kerja perintah (contoh: `tambah`, bukan `menambahkan`).
- **Karakter**: Baris pertama (header) maksimal 70-100 karakter.
- **Keamanan**: Jangan pernah mengunggah file `.env` yang berisi kredensial [Sumber: Prosedur Keamanan].
- **Baseline**: Jika commit menyangkut eksperimen, sertakan referensi issue dan nama dataset atau protokol yang dipakai.
- **Review**: Untuk perubahan besar, lakukan pemeriksaan cepat pada dokumentasi sebelum push.

---

### Tips (Pemula)
Karena penggunaan banyak `-m`, ingatlah aturan emas ini:
1.  **`-m` Pertama**: Adalah **Header** (Wajib ada). Isinya: `type(scope): emoji deskripsi singkat`.
2.  **`-m` Kedua**: Adalah **Body**. Di sini bisa bercerita *kenapa* perubahan itu dilakukan.
3.  **`-m` Ketiga**: Adalah **Footer**. Digunakan untuk menutup issue, contoh: `Closes #7` atau `ref #7`.

Terima kasih telah menjaga standar profesionalitas TME-CORE!

