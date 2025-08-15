from proxmoxer import ProxmoxAPI
import proxmoxer
import typer

proxmox: ProxmoxAPI

import typer
from commands import test as testmod
from commands import setup_networks, migrate, login
from commands.syssec import syssec

app = typer.Typer()

app.add_typer(syssec.app, name="syssec")
app.add_typer(testmod.app, name="test")
app.add_typer(login.app, name="login")
app.add_typer(setup_networks.app, name="setupnetworks")
app.add_typer(migrate.app, name="migrate")

if __name__ == "__main__":
    app()