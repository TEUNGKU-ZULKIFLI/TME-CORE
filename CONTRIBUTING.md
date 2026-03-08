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

---

### Tips (Pemula)
Karena penggunaan banyak `-m`, ingatlah aturan emas ini:
1.  **`-m` Pertama**: Adalah **Header** (Wajib ada). Isinya: `type(scope): emoji deskripsi singkat`.
2.  **`-m` Kedua**: Adalah **Body**. Di sini bisa bercerita *kenapa* perubahan itu dilakukan.
3.  **`-m` Ketiga**: Adalah **Footer**. Digunakan untuk menutup issue, contoh: `Closes #7` atau `ref #7`.

Terima kasih telah menjaga standar profesionalitas TME-CORE!

