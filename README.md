<p align="center">
    <picture>
      <source media="(prefers-color-scheme: light)" srcset="./assets/logos/TME-logo01.png" />
      <img src="./assets/logos/TME-logo01.png" />
  </picture>
</p>
<h1 align="center">
  <span>TME-CORE</span>
  <br align="center">Teungku Mitigation Engine - Core</br>
</h1>
<h3 align="center">
  <a href="./docs/getting_started.md">🚀 Getting Starting</a>
  <span> · </span>
  <a href="./docs/all-tahapan.md">📑 Documentation</a>
  <span> · </span>
  <a href="#-apa-itu-tme-core">ℹ️ Apa itu TME-CORE</a>
  <span> · </span>
  <a href="#-cara-kerja-tme-core">⚙️ Cara Kerja</a>
  <span> · </span>
  <a href="#-persyaratan-sistem">💻 Persyaratan Sistem</a>
  <span> · </span>
  <a href="#-fitur-utama">✨ Fitur Utama</a>
  <span> · </span>
  <a href="#-tujuan">🎯 Tujuan</a>
  <span> · </span>
  <a href="#-installasi">📥 Installasi</a>
</h3>

---

## Apa itu TME-CORE
TME-CORE adalah sistem mitigasi otomatis untuk serangan **Brute Force SSH/FTP** pada Router MikroTik.
Engine berbasis **Python** ini berjalan di server Debian, menganalisa log secara real-time, mendeteksi anomali, dan melakukan blocking otomatis via API RouterOS dengan latency < 5 detik ⚡.

---

## Cara Kerja TME-CORE
1. 📖 Engine membaca log dari Router MikroTik.
2. 🔍 Mendeteksi pola serangan brute force.
3. 🚨 Mengirim perintah blocking ke RouterOS API.
4. ⏱️ Semua proses berlangsung dalam < 5 detik.

---

## Persyaratan Sistem
- 🐧 Debian/Ubuntu Server
- 🐍 Python 3.x
- 🌐 Akses API RouterOS
- 📦 Paket `requests`, `paramiko`, dll.

---

## ✨ Fitur Utama
- 🔎 Analisis log real-time
- 🛡️ Deteksi brute force otomatis
- ⚡ Blocking cepat via API
- 🔗 Integrasi langsung dengan RouterOS

---

## 🎯 Tujuan
Memberikan perlindungan ekstra pada Router MikroTik dengan cara yang **ringan, cepat, dan menyenangkan** untuk sysadmin yang ingin tidur lebih nyenyak 😴.

---

## 📥 Installasi
