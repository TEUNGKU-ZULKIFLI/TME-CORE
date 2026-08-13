# ==========================================
# FILE: src/firewall/mitigator_jalur_a.py
# FUNGSI: Jalur A - Mengeksekusi pemblokiran IP & Putus Sesi
# ==========================================

from typing import Dict, Any

class MitigatorJalurA:
    def __init__(self, address_list_name: str = "brute_force_block", block_timeout: str = "24h"):
        self.address_list_name = address_list_name
        self.block_timeout = block_timeout

    def block_ip_address_list(self, api_connection, ip: str, comment: str = "TME-CORE Auto Block") -> bool:
        try:
            address_list_resource = api_connection.get_resource('/ip/firewall/address-list')

            # Cek apakah IP sudah terdaftar di address-list
            existing = address_list_resource.get(list=self.address_list_name, address=ip)
            if existing:
                print(f"[!] IP {ip} sudah ada di Address-List '{self.address_list_name}'.")
                return True

            # Tambahkan IP ke address-list
            address_list_resource.add(
                list=self.address_list_name,
                address=ip,
                timeout=self.block_timeout,
                comment=comment
            )
            print(f"[✓] IP {ip} BERHASIL ditambahkan ke Address-List '{self.address_list_name}' (Timeout: {self.block_timeout}).")
            return True

        except Exception as e:
            print(f"[✗] Gagal menambahkan IP {ip} ke Address-List: {e}")
            return False

    def kill_active_session(self, api_connection, ip: str) -> int:
        killed_count = 0
        try:
            # Akses menu /ip/firewall/connection
            connection_resource = api_connection.get_resource('/ip/firewall/connection')

            # Cari semua koneksi yang berasal dari IP penyerang (Format: IP:PORT)
            all_connections = connection_resource.get()

            for conn in all_connections:
                src_address = conn.get('src-address', '')
                if src_address.startswith(ip + ":"):
                    conn_id = conn.get('id')
                    # Hapus koneksi aktif ini
                    connection_resource.remove(id=conn_id)
                    killed_count += 1

            if killed_count > 0:
                print(f"[⚡] SESI DIPUTUS: {killed_count} koneksi aktif dari IP {ip} berhasil dihancurkan secara paksa!")
            else:
                print(f"[*] Tidak ada state koneksi aktif yang perlu dihapus untuk IP {ip}.")

        except Exception as e:
            print(f"[✗] Gagal memutus koneksi di firewall untuk IP {ip}: {e}")

        return killed_count

    def execute_mitigation(self, api_connection, threat_data: Dict[str, Any]) -> bool:
        if not threat_data or not api_connection:
            return False

        ip = threat_data.get('ip')
        threat_type = threat_data.get('threat_type')
        service = threat_data.get('service', 'unknown')

        comment_msg = f"TME-CORE: {threat_type} via {service}"

        print(f"\n[🛡️] MENJALANKAN MITIGASI UNTUK IP: {ip} [{threat_type}]")

        # 1. Selalu blokir IP di Firewall Address-List
        block_success = self.block_ip_address_list(api_connection, ip, comment=comment_msg)

        # 2. Jika ancaman berupa UNAUTHORIZED_SUCCESS (Akses Ilegal 1x Tembus), WAJIB Kill Active Session!
        if threat_type == 'UNAUTHORIZED_SUCCESS':
            print(f"[*] Mendeteksi Akses Ilegal Aktif. Mengirim perintah pemutusan sesi ke MikroTik...")
            self.kill_active_session(api_connection, ip)

        return block_success


# --- Blok Testing Mandiri (Tanpa MikroTik Asli) ---
if __name__ == "__main__":
    print("=== TESTING MODUL MITIGATOR JALUR A ===")
    
    # Membuat Objek API Palsu (Mock) agar tidak mengubah router sungguhan saat testing
    class MockResource:
        def get(self, **kwargs):
            if 'address' in kwargs: return [] # Pura-pura IP belum ada di address-list
            return [{'id': '*A1', 'src-address': '192.168.99.99:54321'}] # Pura-pura ada 1 koneksi aktif
        def add(self, **kwargs): pass
        def remove(self, **kwargs): pass
        
    class MockAPI:
        def get_resource(self, path): return MockResource()

    mock_api = MockAPI()
    mitigator = MitigatorJalurA(address_list_name="TEST_BLOCK_LIST", block_timeout="1h")
    
    # Tes Simulasi Brute Force
    threat_brute = {'ip': '10.10.10.10', 'threat_type': 'BRUTE_FORCE', 'service': 'ssh'}
    mitigator.execute_mitigation(mock_api, threat_brute)
    
    # Tes Simulasi Akses Ilegal (Harus memicu pemutusan sesi / Kill Session)
    threat_ilegal = {'ip': '192.168.99.99', 'threat_type': 'UNAUTHORIZED_SUCCESS', 'service': 'winbox'}
    mitigator.execute_mitigation(mock_api, threat_ilegal)
