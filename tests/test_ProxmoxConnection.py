import pytest
import os
from dotenv import load_dotenv

from ubnetdeforchestrator.ProxmoxManager import ProxmoxVMManager

load_dotenv()

# from ubnetdeforchestrator import ProxmoxManager

@pytest.fixture
def proxmox_manager():
    host = os.getenv("PROXMOX_HOST")
    username = os.getenv("PROXMOX_USERNAME")
    password = os.getenv("PROXMOX_PASSWORD")

    # Replace these values with appropriate test credentials and host
    return ProxmoxVMManager(host, username, password)

def test_proxmox_manager_connection(proxmox_manager):
    # Assuming ProxmoxManager has a method `connect` that establishes a connection
    try:
        connection = proxmox_manager
        assert True, "Connection passed without errors"
    except Exception as e:
        pytest.fail(f"Connection failed with error: {e}")