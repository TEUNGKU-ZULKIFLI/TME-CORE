# Draft Update Issue GitHub (Siap Tempel)

Gunakan draf ini untuk memperkaya issue #1-#5 agar lebih terukur.

## Update untuk Issue #1 (Master NDLC)

Tambahkan komentar berikut:

```md
### Update Scope (April 2026)
Konteks perangkat dan infrastruktur saat ini:
- Router fisik: MikroTik hEX RB750Gr2
- Controller: WSL Debian (engine)
- Traffic source: WSL Kali (lab testing)

Deliverables wajib sebelum coding:
- [ ] Baseline jaringan (latency, throughput, packet loss)
- [ ] Baseline CPU router dan stabilitas API
- [ ] Definisi event timestamp untuk MTTR
- [ ] Dokumen protokol pengukuran terstandardisasi

Definition of Done phase 1-3:
- [ ] Semua issue phase punya acceptance criteria terukur
- [ ] Semua skenario uji memiliki bukti data mentah
- [ ] Kriteria Go/No-Go ke fase coding ditetapkan
```

## Update untuk Issue #2 (Analysis)

```md
### Detail Tambahan Analysis
Data yang wajib dikumpulkan:
- Baseline latency (avg, p95)
- Baseline packet loss
- Baseline throughput (Mbps)
- Baseline CPU router (avg, p95)
- API response time dan disconnect rate

Acceptance Criteria tambahan:
- [ ] Minimal 3 run baseline normal
- [ ] Minimal 5 run per skenario serangan
- [ ] Semua event timestamp terdokumentasi
- [ ] Rumus MTTR, ADR, FPR disepakati

Output files:
- docs/MEASUREMENT_PROTOCOL.md
- data/baseline_metrics.csv (opsional)
```

## Update untuk Issue #3 (Design)

```md
### Detail Tambahan Design
Arsitektur final yang dipakai:
- Kali (traffic source) -> Router MikroTik (target) <- Debian (detector/mitigator)

Acceptance Criteria tambahan:
- [ ] Sequence diagram event dari attack sampai block
- [ ] Definisi struktur CSV dan log schema
- [ ] Definisi polling interval dan retry policy API
- [ ] Definisi format alert Telegram
```

## Update untuk Issue #4 (Simulation)

```md
### Detail Tambahan Simulation
Update environment:
- Fokus utama router fisik RB750Gr2 (bukan CHR-only)
- WSL Debian sebagai external engine
- WSL Kali untuk generate traffic uji lab

Acceptance Criteria tambahan:
- [ ] API connection test stabil >= 30 menit
- [ ] Uji threshold jalur A berjalan sesuai target
- [ ] Uji jalur B (anomali) memiliki indikator CPU jelas
- [ ] Data hasil uji tersimpan per run
```

## Update untuk Issue #5 (Security & Documentation)

```md
### Detail Tambahan Security
Hardening awal wajib:
- [ ] Set password admin router (password kosong tidak diperbolehkan)
- [ ] Nonaktifkan service yang tidak dipakai
- [ ] Batasi akses API hanya dari IP controller
- [ ] Simpan kredensial hanya di .env (tidak pernah di-commit)

Acceptance Criteria tambahan:
- [ ] Checklist hardening lengkap
- [ ] Bukti konfigurasi service dan firewall tersedia
- [ ] Struktur logging CSV standar untuk Bab 4
```
