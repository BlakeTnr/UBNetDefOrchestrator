from proxmoxer import ProxmoxAPI
import proxmoxer
import typer
from ProxmoxSysSecStudent import ProxmoxSysSecStudent
from ProxmoxSysSecTeam import ProxmoxSysSecTeam

proxmox: ProxmoxAPI

def main(host: str, username, password, realm = "pve"):
    global proxmox
    try:
        proxmox = ProxmoxAPI(host, user=f'{username}@{realm}', password=password, verify_ssl=False)
    except proxmoxer.AuthenticationError:
        print("Username or password were incorrect!")

    response = proxmox.pools.get()
    print(response)

    for pool in response:
        if(pool['poolid'].startswith("SysSec")):
            print(f"deleting {pool['poolid']}")
            proxmox.pools.delete(pool['poolid'])

    # for i in range(1, 35):
    #     num = str(i)
    #     if i < 10:
    #         num = "0" + str(i)
    #     print(f"Creating SysSecTeam{num}")
    #     proxmox.pools.create(poolid=f"SysSecTeam{num}")

    # team = ProxmoxSysSecTeam(10, proxmox)
    # team.setup()

    setup_syssec()
    user = ProxmoxSysSecStudent("testsyssecstudent", proxmox)
    user.setup()

def setup_syssec():
    for i in range(1, 35):
        syssecTeam = ProxmoxSysSecTeam(i, proxmox)
        syssecTeam.setup()

if __name__ == "__main__":
    typer.run(main)