from proxmoxer import ProxmoxAPI
import proxmoxer
import typer
from ProxmoxSysSecStudent import ProxmoxSysSecStudent
from ProxmoxSysSecTeam import ProxmoxSysSecTeam

proxmox: ProxmoxAPI

import typer
from commands import test as testmod
from commands import setup_networks

app = typer.Typer()

app.add_typer(testmod.app, name="test")
app.add_typer(setup_networks.app, name="setupnetworks")

if __name__ == "__main__":
    app()