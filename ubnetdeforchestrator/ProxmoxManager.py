from ubnetdeforchestrator.ProxmoxLocation import ProxmoxLocation
from ubnetdeforchestrator.MachineManager import MachineManager
from proxmoxer import ProxmoxAPI

class ProxmoxVMManager(MachineManager):
    def __init__(self, host_ip, username, password):
        """
        username: username@realm (e.g., root@pam)
        """

        self.proxmox = ProxmoxAPI(host_ip, user=username, password=password, verify_ssl=False)

    def create_machine(self, node, location, name, cpu, memory, harddrive):
        """
        Create a Proxmox virtual machine with the specified parameters.

        :param name: Name of the virtual machine.
        :param cpu: Number of CPU cores for the VM.
        :param memory: Amount of memory (RAM) for the VM in MB.
        :param harddrive: Size of the hard drive for the VM in GB.
        :return: ID of the created VM.
        """
        
        self.proxmox.nodes('test').qemu.create()
        self.vm_name = name
        self.vm_id = 100

    # def start_vm(self):
    #     print(f"Starting Proxmox machine {self.vm_name} with ID {self.vm_id}")

    # def stop_vm(self):
    #     print(f"Stopping Proxmox machine {self.vm_name} with ID {self.vm_id}")

    # def get_vm_status(self):
    #     print(f"Getting status for Proxmox machine {self.vm_name} with ID {self.vm_id}")
    #     return "Running"