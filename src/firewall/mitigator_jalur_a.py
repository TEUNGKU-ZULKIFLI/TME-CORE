# ==========================================
# FILE: src/firewall/mitigator_jalur_a.py
# FUNGSI: Jalur A - Mengeksekusi pemblokiran IP
# ==========================================
import config.config

def block_ip(api, ip_address):
    """
    Memasukkan IP penyerang ke dalam Address List MikroTik
    untuk di-drop oleh Firewall.
    """
    try:
        address_list = api.get_resource('/ip/firewall/address-list')
        
        # 1. Cek apakah IP sudah ada di daftar blokir agar tidak error duplicate
        existing_lists = address_list.get(address=ip_address, list=config.config.ADDRESS_LIST_NAME)
        
        if len(existing_lists) > 0:
            print(f"[*] MITIGASI: IP {ip_address} sudah berstatus TERBLOKIR sebelumnya.")
            return True
            
        # 2. Eksekusi pemblokiran
        print(f"[!] MITIGASI: Mengeksekusi pemblokiran untuk IP {ip_address}...")
        address_list.add(
            list=config.config.ADDRESS_LIST_NAME,
            address=ip_address,
            timeout=config.config.BLOCK_TIMEOUT,
            comment="Auto-blocked by TME-CORE"
        )
        print(f"[+] SUKSES: IP {ip_address} berhasil dimasukkan ke Address List '{config.config.ADDRESS_LIST_NAME}'")
        return True
        
    except Exception as e:
        print(f"[-] GAGAL MITIGASI: Terjadi error saat memblokir IP {ip_address}")
        print(f"[-] Error: {e}")
        return False