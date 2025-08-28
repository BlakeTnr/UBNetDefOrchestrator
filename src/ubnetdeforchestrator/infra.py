from proxmoxer import ProxmoxAPI
import proxmoxer
import typer

proxmox: ProxmoxAPI

import typer
from commands import test as testmod
from commands import setup_networks, migrate, delete_vms, rename_vms
from commands.syssec import syssec

app = typer.Typer()

app.add_typer(syssec.app, name="syssec")
app.add_typer(testmod.app, name="test")
app.add_typer(setup_networks.app, name="setupnetworks")
app.add_typer(migrate.app, name="migrate")
app.add_typer(delete_vms.app, name="deletevms")
app.add_typer(rename_vms.app, name="renamevms")

if __name__ == "__main__":
    app()