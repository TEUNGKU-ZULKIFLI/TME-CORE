# NDLC Measurement Protocol (Pre-Coding)

Dokumen ini menjadi standar pengukuran untuk fase Analysis/Design/Simulation sebelum implementasi kode utama.

## 1. Tujuan
- Menentukan baseline jaringan dan perangkat sebelum uji brute force terkontrol.
- Mengukur dampak serangan terhadap latency, throughput, packet loss, CPU router.
- Mengukur waktu respons sistem mitigasi (MTTR).

## 2. Lingkungan Uji (Current Plan)
- Router fisik: MikroTik hEX RB750Gr2
- Controller: WSL Debian (engine TME-CORE)
- Traffic source: WSL Kali (generator trafik uji di lab)
- Catatan: Semua pengujian hanya untuk lab berizin.

## 3. Data Wajib Sebelum Coding
- Identitas perangkat:
  - Model router, versi RouterOS, interface aktif.
- Topologi jaringan:
  - Diagram sederhana IP/subnet dan jalur trafik.
- Baseline performa (tanpa serangan):
  - Latency rata-rata dan p95 (ms)
  - Packet loss (%)
  - Throughput (Mbps)
  - CPU router rata-rata dan p95 (%)
- Baseline service behavior:
  - Response time API MikroTik (ms)
  - Stabilitas sesi API (jumlah disconnect per jam)

## 4. Metrik Utama
- MTTR (Mean Time To Respond):
  - Definisi: waktu dari event deteksi valid sampai rule block aktif.
  - Rumus: MTTR = t_block_applied - t_detection
- Alert Latency:
  - Waktu dari t_detection ke pesan Telegram diterima.
- Detection Rate (ADR):
  - ADR = jumlah serangan terdeteksi / total skenario serangan.
- False Positive Rate:
  - FPR = alert pada trafik normal / total alert.

## 5. Event Timestamp Minimum
Simpan semua timestamp dalam UTC+7 atau UTC konsisten.
- t_attack_start
- t_first_failed_login
- t_threshold_reached
- t_detection
- t_block_applied
- t_alert_sent
- t_alert_received

## 6. Skenario Uji Bertahap (Aman)
1) Baseline normal (tanpa serangan).
2) Failed login rendah (di bawah threshold).
3) Failed login cepat (melewati threshold).
4) Successful login + beban CPU tinggi terkontrol.

## 7. Format Output Data
Simpan CSV dengan kolom minimum:
- scenario_id
- run_id
- timestamp
- source_ip
- protocol
- failed_count
- cpu_percent
- latency_ms
- packet_loss_percent
- throughput_mbps
- detection_flag
- block_flag
- mttr_ms
- alert_latency_ms

## 8. Acceptance Criteria Fase Analysis
- Baseline normal terukur minimal 3 kali run.
- Setiap skenario serangan dijalankan minimal 5 run.
- Semua run punya bukti log + CSV.
- Semua metrik punya nilai median + p95.

## 9. Risiko yang Harus Dicatat
- WSL2 networking tidak stabil ke perangkat fisik.
- Router tanpa password admin (risiko sangat tinggi).
- Interferensi trafik kampus menyebabkan baseline bias.

## 10. Keputusan Go/No-Go ke Coding
Go jika:
- Baseline lengkap
- Threshold awal tervalidasi
- Jalur logging dan timestamp konsisten
- Uji API stabil

No-Go jika salah satu belum terpenuhi.
