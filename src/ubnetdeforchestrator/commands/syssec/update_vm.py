import typer
import Proxmox
import proxmoxer
from rich import print
from rich.prompt import Confirm
import sys
from syssec.Team import Team
from ubnetdeforchestrator.ProxmoxInfra import ProxmoxInfra

app = typer.Typer()

@app.callback(invoke_without_command=True)
def update_vm_callback(host, username, password, update, realm="pve"):
    infra = ProxmoxInfra(host, username, password, realm)

    teams = infra.getTeams()

    

    for team in teams:
        infra.deploy_vm(team, vmid)
        # break