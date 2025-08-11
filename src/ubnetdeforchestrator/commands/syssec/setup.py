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
def setup_callback(host, username, password, number_of_teams, realm="pve"):
    confirmed = Confirm.ask(":warning:  This will not teardown any existing teams")
    if not confirmed:
        print("Cancelled")
        sys.quit(1)

    infra = ProxmoxInfra(host, username, password, realm)
    
    for i in range(1, int(number_of_teams)+1):
        team = Team(i)
        infra.createTeam(team)
        print(f":white_check_mark: Created team {i}!")