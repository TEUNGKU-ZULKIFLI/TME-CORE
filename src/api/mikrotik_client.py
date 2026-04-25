"""
MikroTik RouterOS API Client
Wrapper untuk komunikasi dengan RouterOS API (port 8728)
"""

import logging
import time
from typing import Any, Dict, List, Optional

# Third-party imports
import routeros_api
from routeros_api.exceptions import RouterOsApiConnectionError

# Local imports
from src.exceptions import (
    APIConnectionError,
    APITimeoutError,
    APICommandError,
    BlockingError
)

logger = logging.getLogger(__name__)


class MikroTikClient:
    """
    Client untuk RouterOS API dengan error handling dan retry logic

    Fitur:
    - Connect/disconnect dengan retry
    - Execute commands dengan timeout
    - Block/unblock IP addresses
    - Get router resource info (CPU, memory)
    - List address-list entries
    """

    def __init__(
        self,
        host: str,
        username: str,
        password: str,
        port: int = 8728,
        timeout: int = 10,
        address_list_name: str = "brute_force_block"
    ):
        """
        Initialize MikroTik API client

        Args:
            host: IP address dari RouterOS (e.g., 192.168.10.1)
            username: API username (e.g., admin)
            password: API password
            port: API port (default: 8728)
            timeout: Connection timeout dalam seconds (default: 10)
        """
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.timeout = timeout
        self.address_list_name = address_list_name
        self._connection = None
        self._api = None
        self._is_connected = False

        logger.debug(f"MikroTikClient initialized: {host}:{port}")

    def connect(self, retry: int = 3) -> bool:
        """
        Establish connection ke RouterOS API dengan retry logic

        Args:
            retry: Jumlah retry attempts (default: 3)

        Returns:
            True jika koneksi berhasil

        Raises:
            APIConnectionError jika semua retry gagal
        """
        for attempt in range(1, retry + 1):
            try:
                logger.info(f"[Attempt {attempt}/{retry}] Connecting to {self.host}:{self.port}...")

                self._connection = routeros_api.RouterOsApiPool(
                    self.host,
                    username=self.username,
                    password=self.password,
                    port=self.port,
                    plaintext_login=True,
                    use_ssl=False
                    # timeout=self.timeout
                )

                self._api = self._connection.get_api()
                self._is_connected = True

                logger.info(f"✅ Connected to MikroTik {self.host}:{self.port} successfully")
                return True

            except RouterOsApiConnectionError as e:
                logger.warning(f"⚠ Connection attempt {attempt} failed: {e}")
                if attempt < retry:
                    time.sleep(2)  # Wait 2 seconds before retry
                else:
                    raise APIConnectionError(f"Failed to connect after {retry} attempts: {e}")
            except Exception as e:
                logger.error(f"❌ Unexpected error on attempt {attempt}: {e}")
                if attempt < retry:
                    time.sleep(2)
                else:
                    raise APIConnectionError(f"Unexpected error: {e}")

        return False

    def disconnect(self) -> None:
        """Close connection ke RouterOS"""
        try:
            if self._connection:
                self._connection.disconnect()
                self._is_connected = False
                logger.info("✅ Disconnected from MikroTik")
        except Exception as e:
            logger.error(f"❌ Error during disconnect: {e}")

    def execute_command(
        self,
        path: str,
        arguments: Dict[str, str] = None
    ) -> List[Dict]:
        """
        Execute command di RouterOS

        Args:
            path: API path (e.g., "/interface")
            arguments: Query parameters (optional)

        Returns:
            List[Dict] - Response dari RouterOS

        Raises:
            APIConnectionError, APICommandError

        Example:
            interfaces = client.execute_command("/interface")
        """
        if not self._is_connected:
            raise APIConnectionError("Not connected to RouterOS. Call connect() first.")

        try:
            logger.debug(f"Executing command: {path}")
            resource = self._api.get_resource(path)
            response = resource.get(**arguments) if arguments else resource.get()
            logger.debug(f"✅ Command executed successfully: {path}")
            return response

        except Exception as e:
            logger.error(f"❌ Command failed: {path} - {e}")
            raise APICommandError(f"Command failed: {path} - {e}")

    def block_ip(
        self,
        ip_address: str,
        list_name: str = "brute_force_block",
        comment: str = ""
    ) -> bool:
        """
        Block IP address dengan menambahkan ke address-list

        Args:
            ip_address: IP untuk di-block (e.g., "192.168.1.100")
            list_name: Nama address-list (default: "brute_force_block")
            comment: Comment untuk entry (auto-generated jika kosong)

        Returns:
            True jika berhasil

        Raises:
            BlockingError

        Example:
            client.block_ip("192.168.1.100")
        """
        if not comment:
            comment = f"Auto-blocked at {time.strftime('%Y-%m-%d %H:%M:%S')}"

        try:
            start_time = time.time()

            # Get resource dan add entry
            resource = self._api.get_resource('/ip/firewall/address-list')
            resource.add(
                address=ip_address,
                list=list_name,
                comment=comment
            )

            response_time = (time.time() - start_time) * 1000  # Convert ke ms
            logger.info(f"✅ BLOCKED: {ip_address} (response time: {response_time:.2f}ms)")
            return True

        except Exception as e:
            logger.error(f"❌ Blocking failed for {ip_address}: {e}")
            raise BlockingError(f"Failed to block {ip_address}: {e}")

    def unblock_ip(
        self,
        ip_address: str,
        list_name: str = "brute_force_block"
    ) -> bool:
        """
        Remove IP dari address-list (unblock)

        Args:
            ip_address: IP untuk di-unblock
            list_name: Nama address-list

        Returns:
            True jika berhasil

        Raises:
            BlockingError

        Example:
            client.unblock_ip("192.168.1.100")
        """
        try:
            resource = self._api.get_resource('/ip/firewall/address-list')
            entries = resource.get(address=ip_address, list=list_name)

            if not entries:
                logger.warning(f"⚠ No entries found for {ip_address} in {list_name}")
                return True

            for entry in entries:
                resource.remove(id=entry['.id'])

            logger.info(f"✅ UNBLOCKED: {ip_address}")
            return True

        except Exception as e:
            logger.error(f"❌ Unblock failed for {ip_address}: {e}")
            raise BlockingError(f"Failed to unblock {ip_address}: {e}")

    def get_router_cpu(self) -> Dict[str, Any]:
        """
        Get router CPU dan memory info

        Returns:
            Dict dengan keys: cpu_load, cpu_count, free_memory_mb, total_memory_mb

        Raises:
            APICommandError

        Example:
            cpu_info = client.get_router_cpu()
            print(f"CPU Load: {cpu_info['cpu_load']}%")
        """
        try:
            resources = self.execute_command("/system/resource")
            if resources:
                data = resources[0]
                return {
                    "cpu_load": int(data.get("cpu-load", 0)),
                    "cpu_count": int(data.get("cpu-count", 1)),
                    "free_memory_mb": float(data.get("free-memory", "0").rstrip(" MiB")),
                    "total_memory_mb": float(data.get("total-memory", "0").rstrip(" MiB")),
                }
            return {}

        except Exception as e:
            logger.error(f"❌ Failed to fetch CPU info: {e}")
            raise APICommandError(f"Failed to get CPU info: {e}")

    def list_address_lists(self) -> List[Dict]:
        """
        Get semua entries dari address-list

        Returns:
            List[Dict] - Daftar address-list entries

        Raises:
            APICommandError

        Example:
            lists = client.list_address_lists()
            for entry in lists:
                print(f"{entry['address']} - {entry['list']}")
        """
        try:
            return self.execute_command("/ip/firewall/address-list")
        except Exception as e:
            logger.error(f"❌ Failed to list address-lists: {e}")
            raise APICommandError(f"Failed to list address-lists: {e}")

    def list_blocked_ips(self, list_name: str = "brute_force_block") -> List[str]:
        """
        Get daftar IP yang sudah di-block di list tertentu

        Args:
            list_name: Nama address-list (default: "brute_force_block")

        Returns:
            List[str] - Daftar blocked IPs

        Example:
            blocked = client.list_blocked_ips()
            print(f"Blocked IPs: {blocked}")
        """
        try:
            entries = self.execute_command(
                "/ip/firewall/address-list",
                {"?list": list_name}
            )
            ips = [entry.get("address") for entry in entries]
            logger.info(f"Found {len(ips)} blocked IPs in list '{list_name}'")
            return ips

        except Exception as e:
            logger.error(f"❌ Failed to list blocked IPs: {e}")
            raise APICommandError(f"Failed to list blocked IPs: {e}")


# Contoh penggunaan:
# if __name__ == "__main__":
#     from src.config import get_config
#     config = get_config()
#     client = MikroTikClient(**config['mikrotik'])
#     client.connect()
#     print(client.list_address_lists())
#     client.disconnect()