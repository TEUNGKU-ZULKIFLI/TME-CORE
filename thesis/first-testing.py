import routeros_api
from routeros_api.exceptions import RouterOsApiConnectionError, RouterOsApiCommunicationError

def connect_to_mikrotik(host, username, password, port=8728):
    """
    Connects to a MikroTik RouterOS device and returns the API connection object.
    """
    try:
        connection = routeros_api.RouterOsApiPool(
            host,
            username=username,
            password=password,
            port=port,
            plaintext_login=True,  # Set to False if using SSL
            use_ssl=False
        )
        return connection
    except RouterOsApiConnectionError as e:
        print(f"[ERROR] Could not connect to MikroTik: {e}")
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
    return None

def get_interfaces(api):
    """
    Retrieves and prints interface information from the MikroTik device.
    """
    try:
        interface_resource = api.get_resource('/interface')
        interfaces = interface_resource.get()
        print("=== MikroTik Interfaces ===")
        for iface in interfaces:
            print(f"Name: {iface.get('name')}, Type: {iface.get('type')}, Running: {iface.get('running')}")
    except RouterOsApiCommunicationError as e:
        print(f"[ERROR] Communication error: {e}")
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")

if __name__ == "__main__":
    # Replace with your MikroTik credentials
    HOST = "192.168.10.1"
    USERNAME = "admin"
    PASSWORD = "085213"

    connection = connect_to_mikrotik(HOST, USERNAME, PASSWORD)
    if connection:
        api = connection.get_api()
        get_interfaces(api)
        connection.disconnect()
