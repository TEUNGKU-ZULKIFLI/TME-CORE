#!/bin/bash
# =========================================================
# TME-CORE UNINSTALLATION SCRIPT
# =========================================================

echo "████████╗███╗   ███╗███████╗     ██████╗ ██████╗ ██████╗ ███████╗"
echo "╚══██╔══╝████╗ ████║██╔════╝    ██╔════╝██╔═══██╗██╔══██╗██╔════╝"
echo "   ██║   ██╔████╔██║█████╗█████╗██║     ██║   ██║██████╔╝█████╗  "
echo "   ██║   ██║╚██╔╝██║██╔══╝╚════╝██║     ██║   ██║██╔══██╗██╔══╝  "
echo "   ██║   ██║ ╚═╝ ██║███████╗    ╚██████╗╚██████╔╝██║  ██║███████╗"
echo "   ╚═╝   ╚═╝     ╚═╝╚══════╝     ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝"
echo "                                                                 "
echo "================================================================="
echo "        🗑️ Memulai Uninstalasi Service TME-CORE..."
echo "================================================================="

# Memastikan Engine service berhenti
sudo systemctl stop tmecore.service &&
# Mulai Mematikan Engine service
sudo systemctl disable tmecore.service &&
# Mulai Menghapus Engine service
sudo rm -rf /etc/systemd/system/tmecore.service &&
# Memuat Ulang SystemD
sudo systemctl daemon-reload &&
sudo systemctl daemon-reload &&
sudo systemctl daemon-reload &&
# Validasi Engine Service
sudo systemctl status tmecore.service &&
# Vacum log
sudo journalctl --unit=tmecore.service --vacuum-time=1s

echo "████████╗███╗   ███╗███████╗     ██████╗ ██████╗ ██████╗ ███████╗"
echo "╚══██╔══╝████╗ ████║██╔════╝    ██╔════╝██╔═══██╗██╔══██╗██╔════╝"
echo "   ██║   ██╔████╔██║█████╗█████╗██║     ██║   ██║██████╔╝█████╗  "
echo "   ██║   ██║╚██╔╝██║██╔══╝╚════╝██║     ██║   ██║██╔══██╗██╔══╝  "
echo "   ██║   ██║ ╚═╝ ██║███████╗    ╚██████╗╚██████╔╝██║  ██║███████╗"
echo "   ╚═╝   ╚═╝     ╚═╝╚══════╝     ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝"
echo "                                                                 "
echo "================================================================="
echo "              ✅ UNINSTALASI SERVICE TME-CORE SELESAI!"
echo "-----------------------------------------------------------------"
echo "👉 Langkah Selanjutnya:"
echo "1. Memeriksa kembali service tmecore: sudo systemctl status tmecore.service"
echo "==========================================================================="
