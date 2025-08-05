from SysSecTeam import SysSecTeam
from proxmoxer import ProxmoxAPI

class ProxmoxSysSecTeam(SysSecTeam):
    def __init__(self, team_number: int, proxmox: ProxmoxAPI):
        super().__init__(team_number)
        self.proxmox = proxmox

    def _create_pool(self):
        poolid = f"SysSecTeam{self.team_number}"

        if(self.team_number <= 9):
            poolid = f"SysSecTeam0{self.team_number}"
            
        self.proxmox.pools.create(poolid=poolid)
        print(f"Creating {poolid}")

    def _create_hidden_pool(self):
        poolid = f"SysSecTeam{self.team_number}"

        if(self.team_number <= 9):
            poolid = f"SysSecTeam0{self.team_number}_hidden"
            
        self.proxmox.pools.create(poolid=poolid)
        print(f"Creating {poolid}")

    def setup(self):
        self._create_pool()
        self._create_hidden_pool()
        