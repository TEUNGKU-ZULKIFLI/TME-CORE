from typing import Dict, Any

class MitigatorJalurA:
    def __init__(self, address_list_name: str = "brute_force_block", block_timeout: str = "24h"):
        self.address_list_name = address_list_name
        self.block_timeout = block_timeout

    def block_ip_address_list(self, api_connection, ip: str, comment: str = "TME-CORE Auto Block") -> bool:
        try:
            address_list_resource = api_connection.get_resource('/ip/firewall/address-list')
            
            existing = address_list_resource.get(list=self.address_list_name, address=ip)
            if existing:
                print(f"[!] IP {ip} sudah ada di Address-List '{self.address_list_name}'.")
                return True

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
            connection_resource = api_connection.get_resource('/ip/firewall/connection')
            all_connections = connection_resource.get()

            for conn in all_connections:
                src_address = conn.get('src-address', '')
                if src_address.startswith(ip + ":"):
                    conn_id = conn.get('id')
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

        block_success = self.block_ip_address_list(api_connection, ip, comment=comment_msg)

        if threat_type == 'UNAUTHORIZED_SUCCESS':
            print(f"[*] Mendeteksi Akses Ilegal Aktif. Mengirim perintah pemutusan sesi ke MikroTik...")
            self.kill_active_session(api_connection, ip)

        return block_success
