from proxmoxer import ProxmoxAPI
import proxmoxer
import typer
from ProxmoxSysSecStudent import ProxmoxSysSecStudent
from ProxmoxSysSecTeam import ProxmoxSysSecTeam

proxmox: ProxmoxAPI

import typer
from commands import test as testmod

app = typer.Typer()

app.add_typer(testmod.app, name="test")

if __name__ == "__main__":
    app()