from syssec.Infra import Infra
from syssec.Student import Student
from syssec.Team import Team
import proxmoxer
from rich import print
import math

class ProxmoxInfra(Infra):
    def __init__(self, host, username, password, realm="pve"):
        try:
            self.proxmox = proxmoxer.ProxmoxAPI(host, user=f'{username}@{realm}', password=password, verify_ssl=False, timeout=None)
        except proxmoxer.AuthenticationError:
            print(":x: Username or password were incorrect!")
            quit()

    def createStudent(self, student: Student, password: str=None):
        self.proxmox.access.users.create(userid=f"{student.identifier}@pve", password=password, comment="SysSec Student Fall 2025")

    def _create_pool(self, team: Team):
            poolid = f"SysSecTeam{team.team_number}"

            if(team.team_number <= 9):
                poolid = f"SysSecTeam0{team.team_number}"
                
            self.proxmox.pools.create(poolid=poolid)
            print(f"Creating {poolid}")

    def _create_hidden_pool(self, team: Team):
        poolid = f"SysSecTeam{team.team_number}_hidden"

        if(team.team_number <= 9):
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
                teamName = int(teamName)
                if teamName not in sysSecTeams:
                    sysSecTeams.append(int(teamName))
        
        teams = []
        for sysSecTeam in sysSecTeams:
            team = Team(sysSecTeam)
            teams.append(team)

        return teams

    def createTeam(self, team: Team):
        self._create_pool(team)
        self._create_hidden_pool(team)

    def deleteTeam(self, team: Team):
        self.proxmox.pools(self._get_pool_name(team)).delete()
        self.proxmox.pools(f"{self._get_pool_name(team)}_hidden").delete()

    def deploy_vm(self, team: Team, vmIdentifier: str):
        '''
        vmIdentifier is the id of the vm for proxmox
        '''
        nextid = self.proxmox.cluster.nextid.get()
        vm = self._find_template_for_team(team, vmIdentifier)
        vhost = self._get_vhost_of_team(team)

        # TODO: THIS NEEDS TO BE CHANGED TO BE DYNAMIC
        print(f"Deploying {vm['vmid']} which is {vm['name']} to {vhost} for team {team.team_number}")
        # print(f"Pool name {self._get_pool_name(team)}")
        self.proxmox(f"nodes/{vhost}/{self._get_vm_type(vm)}/{vm['vmid']}/clone").post(newid=nextid, name=f"{vm['name']}-deployed", pool=self._get_pool_name(team))
    
    def _find_template_for_team(self, team: Team, vmIdentifier: str):
        vm = self._find_vm(vmIdentifier)
        vm_name = vm['name']
        nextid = self.proxmox.cluster.nextid.get()
        vhost = self._get_vhost_of_team(team)
        
        qemus = self.proxmox.nodes(vhost).qemu.get()
        lxcs = self.proxmox.nodes(vhost).lxc.get()

        foundQemus = []
        for qemu in qemus:
            if(qemu['name'] == vm_name):
                foundQemus.append(qemu)
        
        foundLxcs = []
        for lxc in lxcs:
            if(lxc['name'] == vm_name):
                foundLxcs.append(lxc)

        if(len(foundQemus) > 0 and len(foundLxcs) > 0):
            raise Exception(f"Couldn't find unique vm for {vm_name} on host {vhost}")
        
        if(len(foundQemus) > 1 or len(foundLxcs) > 1):
            raise Exception(f"Couldn't find unique vm for {vm_name} on host {vhost}")
        
        if(len(foundQemus) == 1):
            return foundQemus[0]
        elif(len(foundLxcs) == 1):
            return foundLxcs[0]
        else:
            raise Exception(f"Couldn't find any vm for {vm_name} on host {vhost}")
    
    def _get_vhost_of_team(self, team: Team):
        vhosts = ['cdr-vhost2', 'cdr-vhost4', 'cdr-vhost5', 'cdr-vhost6']
        teams_per_host = 35/len(vhosts)
        team_vhost_index = math.floor(team.team_number/(teams_per_host + 0.001)) # 0.001 is to prevent it from going to next index, so instead of 4 we get 3.9999 so floor works
        team_vhost = vhosts[team_vhost_index]
        return team_vhost

    def _get_pool_name(self, team: Team):
        name = "SysSecTeam"
        print(team.team_number)
        if(team.team_number <= 9):
            name += '0'
        name += str(team.team_number)
        return name

    def _get_vm_type(self, vm):
        try:
            return vm['type']
        except KeyError:
            return 'qemu'

    def _find_vm(self, vmIdentifier: str):
        for node in self.proxmox.nodes.get():
            node_name = node["node"]

            # Check QEMU VMs
            qemus = self.proxmox.nodes(node_name).qemu.get()
            for vm in qemus:
                if str(vm["vmid"]) == str(vmIdentifier):
                    return vm

            # Check LXC containers
            lxcs = self.proxmox.nodes(node_name).lxc.get()
            for vm in lxcs:
                if str(vm["vmid"]) == str(vmIdentifier):
                    return vm

        return None

    def _get_student(self, student: Student):
        student = self.proxmox.access.users(f"{student.identifier}@pve").get()
        return student

    def _get_team(self, team: Team):
        pool = self.proxmox.pools(f"SysSecTeam{team.team_number if team.team_number >= 10 else '0' + str(team.team_number)}").get()
        return pool

    def assignStudentToTeam(self, student: Student, team: Team):

        proxmoxTeam = self._get_team(team)

        self.proxmox.access.acl.put(
            path=f"/pool/SysSecTeam{team.team_number if team.team_number >= 10 else '0' + str(team.team_number)}",   # path to pool
            users=f"{student.identifier}@pve",       # user
            roles="SysSec"      # role to assign
        )

    def updateNetwork():
        pass