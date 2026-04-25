"""
Custom exceptions untuk TME-CORE
Digunakan untuk error handling yang lebih spesifik
"""

class TMECoreException(Exception):
    """Base exception class untuk semua error di TME-CORE"""
    pass


class APIConnectionError(TMECoreException):
    """Exception ketika koneksi ke RouterOS API gagal"""
    pass


class APITimeoutError(TMECoreException):
    """Exception ketika API request timeout"""
    pass


class APICommandError(TMECoreException):
    """Exception ketika API command gagal di-execute"""
    pass


class BlockingError(TMECoreException):
    """Exception ketika blocking action (add to address-list) gagal"""
    pass


class ParsingError(TMECoreException):
    """Exception ketika parsing log file gagal"""
    pass


class ConfigError(TMECoreException):
    """Exception ketika loading config gagal"""
    pass


# Contoh penggunaan:
# try:
#     api.connect()
# except APIConnectionError as e:
#     logger.error(f"Connection failed: {e}")
#     raise