# Data Layout

Struktur ini dipakai agar data lab rapi dan aman.

## Folder
- `raw/`: data mentah dari lab (default jangan dipush jika sensitif/besar).
- `processed/`: data yang sudah dibersihkan dan siap analisis.
- `templates/`: template CSV agar format konsisten antar eksperimen.

## Aturan Praktis
- Simpan bukti mentah (log lengkap/screenshot besar) di storage lokal kampus jika ukurannya besar.
- Commit hanya dataset yang sudah diseleksi untuk laporan.
- Jangan simpan kredensial, token, atau IP sensitif yang tidak perlu dipublikasi.
