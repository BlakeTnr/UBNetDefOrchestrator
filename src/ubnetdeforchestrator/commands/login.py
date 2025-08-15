import typer
import Proxmox
import proxmoxer
from rich import print

from ProxmoxInfra import ProxmoxInfra

app = typer.Typer()

@app.callback(invoke_without_command=True)
def login_callback(host, username, password, realm="pve"):
    infra = ProxmoxInfra(host, username, password, realm)

    response = infra.proxmox.access.users(f"{username}@{realm}").token("testtoken").create(
        expire=0,  # 0 means never expire
        comment="UBInfra CLI token"
    )
    
    token = response.value

    