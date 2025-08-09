import typer
import Proxmox
import proxmoxer
from rich import print

app = typer.Typer()

@app.callback(invoke_without_command=True)
def migrate_callback(fromnode, tonode, host, username, password, realm="pve"):
    proxmoxInstance: proxmoxer.ProxmoxAPI = Proxmox.get_proxmox_instance(host, username, password)

    node = proxmoxInstance.nodes(fromnode)

    node.migrateall.post(node=fromnode, target=tonode)