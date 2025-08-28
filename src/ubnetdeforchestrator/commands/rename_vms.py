import typer
import Proxmox
import proxmoxer
from rich import print

app = typer.Typer()

@app.callback(invoke_without_command=True)
def renamevms_callback(host, username, password, oldname, newname, realm="pve"):
    proxmox: proxmoxer.ProxmoxAPI = Proxmox.get_proxmox_instance(host, username, password)

    nodes = proxmox.nodes.get()

    for node in nodes:
        nodeName = node['node']

        qemus = proxmox.nodes(nodeName).qemu.get()
        lxcs = proxmox.nodes(nodeName).lxc.get()

        for qemu in qemus:
            if(qemu['name'] == oldname):
                print(f"Renaming {qemu['name']} ({qemu['vmid']}) to {newname}")
                proxmox.nodes(nodeName).qemu(qemu['vmid']).config.put(name=newname)

        for lxc in lxcs:
            if(lxc['name'] == oldname):
                print(f"Renaming {lxc['name']} ({lxc['vmid']}) to {newname}")
                proxmox.nodes(nodeName).lxc(lxc['vmid']).config.put(name=newname)