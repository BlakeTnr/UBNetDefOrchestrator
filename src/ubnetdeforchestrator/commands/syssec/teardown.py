import typer
import Proxmox
import proxmoxer
from rich import print
from rich.prompt import Confirm
import sys
from ubnetdeforchestrator.ProxmoxInfra import ProxmoxInfra

app = typer.Typer()

@app.callback(invoke_without_command=True)
def teardown_callback(host, username, password, realm="pve"):
    confirmed = Confirm.ask(":warning:  This is irreversible! This will delete all of syssec. Are you sure?")
    if not confirmed:
        print("Cancelled")
        sys.quit(1)

    infra = ProxmoxInfra(host, username, password, realm)
    
    teams = infra.getTeams()
    
    for team in teams:
        try:
            infra.deleteTeam(team)
            print(f"Deleted team {team.team_number}")
        except Exception as e:
            print(f"Couldn't delete team {team.team_number} because {e}")