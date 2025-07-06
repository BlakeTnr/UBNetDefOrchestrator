from ubnetdeforchestrator.MachineManager import MachineManager
from proxmoxer import ProxmoxAPI

class ProxmoxVMManager(MachineManager):
    def __init__(self, host_ip, username, password):
        """
        username: username@realm (e.g., root@pam)
        """

        proxmox = ProxmoxAPI(host_ip, user=username, password=password, verify_ssl=False)
        self.vm_type = "Proxmox"

    def start_vm(self):
        print(f"Starting Proxmox machine {self.vm_name} with ID {self.vm_id}")

    def stop_vm(self):
        print(f"Stopping Proxmox machine {self.vm_name} with ID {self.vm_id}")

    def get_vm_status(self):
        print(f"Getting status for Proxmox machine {self.vm_name} with ID {self.vm_id}")
        return "Running"