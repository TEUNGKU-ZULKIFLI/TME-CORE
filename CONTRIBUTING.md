# Panduan Kontribusi TME-CORE

Terima kasih telah berkontribusi pada **TME-CORE (Traffic Mitigation External Core)**. Dokumen ini bertujuan untuk menjaga kerapian repository agar setiap perubahan terdokumentasi secara profesional, konsisten, dan memiliki jejak audit yang jelas (*audit trail*).

---

## 🚀 Standar Pesan Commit (Semantic Commits)

Kita menggunakan format **Conventional Commits** untuk memastikan sejarah (*history*) proyek tetap bersih dan mudah dibaca oleh pengembang lain.

```bash
<type>(<scope>): <emoji> <deskripsi singkat dalam Bahasa Indonesia> [ref #N | close #N]
```

### 1. Daftar Type Commit
| Type | Emoji | Kegunaan |
| :--- | :---: | :--- |
| **feat** | ✨ | Penambahan fitur baru (misal: logika mitigasi cerdas) |
| **fix** | 🐛 | Perbaikan bug atau kesalahan logika pada sistem |
| **docs** | 📚 | Perubahan pada dokumentasi (README, komentar kode, manual) |
| **style** | 🎨 | Perapian kode (formatting, PEP 8) tanpa mengubah logika |
| **refactor** | ♻️ | Restrukturisasi kode agar lebih modular dan efisien |
| **test** | ✅ | Penambahan skenario uji atau validasi fungsi sistem |
| **chore** | 🔧 | Tugas rutin (update library, .gitignore, konfigurasi env) |

### 2. Daftar Scope Berbasis NDLC
Gunakan *scope* ini untuk memperjelas fase pengembangan mana yang sedang dikerjakan sesuai metodologi sistem:

- **analysis**: Identifikasi pola log serangan, penetapan threshold, dan definisi metrik performa.
- **design**: Perancangan arsitektur engine (IPO), diagram topologi, dan alur logika flowchart.
- **simulation**: Persiapan lingkungan virtual (test-bed), instalasi CHR, dan pengujian koneksi API dasar.
- **implementation**: Proses pengodean utama Python, integrasi API MikroTik, dan Bot Telegram.
- **monitoring**: Simulasi serangan aktif (A/B Testing) dan pengambilan data metrik real-time.
- **management**: Evaluasi data hasil pengujian, pengolahan laporan teknis, dan optimasi sistem.

---

## 🛠️ Alur Kerja (Workflow)

1. **Sinkronisasi**: Selalu lakukan `git pull origin main` sebelum mulai bekerja untuk menghindari konflik kode.
2. **Issue Tracking**: Pilih salah satu Sub-Issue pada GitHub (misal #2 untuk fase Analysis) yang akan dikerjakan.
3. **Commit**: Gunakan pesan commit yang semantik.
   - Contoh: `feat(implementation): ✨ tambah modul ekstraksi log via api port 8728 ref #4`
   - Contoh: `docs(design): 📚 perbarui diagram topologi jaringan pada readme close #3`
4. **Push**: Kirim perubahan kamu ke repository pusat dengan `git push origin main`.

---

## 📝 Catatan Penting
- **Standar Kode**: Pastikan kode Python mengikuti standar PEP 8 (indentasi 4 spasi).
- **Keamanan**: **Dilarang keras** melakukan commit pada file `.env` yang berisi kredensial nyata. Selalu gunakan file `.env.example` sebagai referensi konfigurasi.
- **Metrik**: Pastikan setiap perubahan pada *logic* tetap mengacu pada target efisiensi MTTR < 5 detik.

Terima kasih telah menjaga profesionalitas pengembangan TME-CORE!
