from SysSecStudent import SysSecStudent
from proxmoxer import ProxmoxAPI
from ProxmoxSysSecTeam import ProxmoxSysSecTeam

class ProxmoxSysSecStudent(SysSecStudent):
    def __init__(self, identifier: str, proxmox: ProxmoxAPI):
        self.identifier = identifier
        self.proxmox = proxmox
    
    def setup(self):
        self.proxmox.access.users.create(userid=f"{self.identifier}@pve")

    def assign_to_team(self, ProxmoxSysSecTeam: ProxmoxSysSecTeam):
        # self.proxmox.
        pass