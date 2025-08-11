from syssec.Infra import Infra
from syssec.Student import Student
from syssec.Team import Team
import proxmoxer
from rich import print

class ProxmoxInfra(Infra):
    def __init__(self, host, username, password, realm="pve"):
        try:
            self.proxmox = proxmoxer.ProxmoxAPI(host, user=f'{username}@{realm}', password=password, verify_ssl=False, timeout=None)
        except proxmoxer.AuthenticationError:
            print(":x: Username or password were incorrect!")
            quit()

    def createStudent(self, student: Student):
        self.proxmox.access.users.create(userid=f"{self.identifier}@pve")

    def _create_pool(self, team: Team):
            poolid = f"SysSecTeam{team.team_number}"

            if(team.team_number <= 9):
                poolid = f"SysSecTeam0{team.team_number}"
                
            self.proxmox.pools.create(poolid=poolid)
            print(f"Creating {poolid}")

    def _create_hidden_pool(self, team: Team):
        poolid = f"SysSecTeam{team.team_number}"

        if(self.team_number <= 9):
            poolid = f"SysSecTeam0{team.team_number}_hidden"
            
        self.proxmox.pools.create(poolid=poolid)
        print(f"Creating {poolid}")

    def getTeams(self) -> list[Team]:
        pools = self.proxmox.pools.get()
        sysSecTeams = []
        for pool in pools:
            poolName: str = pool['poolid']
            if poolName.startswith("SysSecTeam"):
                teamName = poolName.removeprefix("SysSecTeam")
                teamName = teamName[0:2]
                if teamName not in sysSecTeams:
                    sysSecTeams.append(teamName)
        
        teams = []
        for sysSecTeam in sysSecTeams:
            team = Team(sysSecTeam)
            teams.append(team)

        return teams

    def createTeam(self, team: Team):
        self._create_pool(team)
        self._create_hidden_pool(team)

    def deleteTeam(self, team: Team):
        self.proxmox.pools(f"SysSecTeam{team.team_number}").delete()
        self.proxmox.pools(f"SysSecTeam{team.team_number}_hidden").delete()

    def _get_student(self, student: Student):
        student = self.proxmox.access.users(f"{student.identifier}@pve")
        return student
    
    def _get_team(self, team: Team):
        pool = self.proxmox.pools(f"SysSecTeam{team.team_number}").get()
        return pool

    def assignStudentToTeam(self, student: Student, team: Team):
        proxmoxUser = self._get_student(student)
        proxmoxTeam = self._get_team(team)
        
        raise Exception("Assign student to team function not finished")
