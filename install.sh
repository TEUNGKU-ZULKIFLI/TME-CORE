#!/bin/bash
# =========================================================
# TME-CORE INSTALLATION SCRIPT
# =========================================================

echo "████████╗███╗   ███╗███████╗     ██████╗ ██████╗ ██████╗ ███████╗"
echo "╚══██╔══╝████╗ ████║██╔════╝    ██╔════╝██╔═══██╗██╔══██╗██╔════╝"
echo "   ██║   ██╔████╔██║█████╗█████╗██║     ██║   ██║██████╔╝█████╗  "
echo "   ██║   ██║╚██╔╝██║██╔══╝╚════╝██║     ██║   ██║██╔══██╗██╔══╝  "
echo "   ██║   ██║ ╚═╝ ██║███████╗    ╚██████╗╚██████╔╝██║  ██║███████╗"
echo "   ╚═╝   ╚═╝     ╚═╝╚══════╝     ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝"
echo "                                                                 "
echo "================================================================="
echo "        🛡️ Memulai Instalasi Lingkungan TME-CORE..."
echo "================================================================="

# 1. Validasi Python
if ! command -v python3 &> /dev/null; then
    echo "[-] Python3 tidak terdeteksi! Silakan instal Python3 terlebih dahulu."
    exit 1
fi

# 2. Setup Virtual Environment
echo "[+] 1. Menyiapkan Virtual Environment (venv)..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "   -> venv berhasil dibuat."
else
    echo "   -> venv sudah ada. Melewati tahap ini."
fi

# 3. Instalasi Pustaka
echo "[+] 2. Menginstal Pustaka Python (requirements.txt)..."
./venv/bin/pip install -r requirements.txt --upgrade pip

# 4. Inisialisasi Kredensial (.env)
echo "[+] 3. Mengatur file konfigurasi (.env)..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "   -> File .env berhasil di-generate dari template."
    echo "   -> [!!!] PERHATIAN: Silakan edit file .env dan isi dengan IP & Password MikroTik Anda!"
else
    echo "   -> File .env sudah ada. Kredensial Anda aman."
fi

# 5. Persiapan Folder Data
echo "[+] 4. Menyiapkan folder penyimpanan log..."
mkdir -p data
touch data/.gitkeep

echo "████████╗███╗   ███╗███████╗     ██████╗ ██████╗ ██████╗ ███████╗"
echo "╚══██╔══╝████╗ ████║██╔════╝    ██╔════╝██╔═══██╗██╔══██╗██╔════╝"
echo "   ██║   ██╔████╔██║█████╗█████╗██║     ██║   ██║██████╔╝█████╗  "
echo "   ██║   ██║╚██╔╝██║██╔══╝╚════╝██║     ██║   ██║██╔══██╗██╔══╝  "
echo "   ██║   ██║ ╚═╝ ██║███████╗    ╚██████╗╚██████╔╝██║  ██║███████╗"
echo "   ╚═╝   ╚═╝     ╚═╝╚══════╝     ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝"
echo "                                                                 "
echo "================================================================="
echo "              ✅ INSTALASI TME-CORE SELESAI!"
echo "-----------------------------------------------------------------"
echo "👉 Langkah Selanjutnya:"
echo "1. Edit kredensial Anda: nano .env"
echo "2. Uji coba koneksi: source venv/bin/activate && python3 -m src.api.connection"
echo "3. Atau Jalankan Langsung Engine: source venv/bin/activate && python3 -m src.main_engine"
echo "========================================================================================"
