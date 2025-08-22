import typer
import Proxmox
import proxmoxer
from rich import print

app = typer.Typer()

@app.callback(invoke_without_command=True)
def migrate_callback(host, username, password, vmname, realm="pve"):
    proxmox: proxmoxer.ProxmoxAPI = Proxmox.get_proxmox_instance(host, username, password)

    nodes = proxmox.nodes.get()

    for node in nodes:
        nodeName = node['node']

        qemus = proxmox.nodes(nodeName).qemu.get()
        lxcs = proxmox.nodes(nodeName).lxc.get()

        for qemu in qemus:
            if(qemu['name'] == vmname):
                print(f"Deleting {qemu['name']}")
                proxmox.nodes(nodeName).qemu(qemu['vmid']).delete()

        for lxc in lxcs:
            if(lxc['name'] == vmname):
                print(f"Deleting {qemu['name']}")
                proxmox.nodes(nodeName).lxc(lxc['vmid']).delete()