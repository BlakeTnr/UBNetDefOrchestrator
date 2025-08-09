import typer
import Proxmox
import proxmoxer
from rich import print

app = typer.Typer()

@app.callback(invoke_without_command=True)
def setupnetworks_callback(host, username, password, realm="pve"):
    proxmoxInstance: proxmoxer.ProxmoxAPI = Proxmox.get_proxmox_instance(host, username, password)
    nodes = proxmoxInstance.nodes.get()
    
    for node in nodes:
        nodeName = node['node']
        nodeStatus = node['status']

        if nodeStatus != "online":
            print(f":warning:  host {nodeName} is {nodeStatus}, skipping...")
            continue

        networks = proxmoxInstance.nodes(nodeName).network.get()
        print(networks)

        ethNetworks = []
        bridgeNetworks = []
        for network in networks:
            if(network['type'] == "eth"):
                ethNetworks.append(network)
            if(network['type'] == "bridge"):
                bridgeNetworks.append(network)

        bridgesToCheckNames = []
        bridgesToCheck = {}
        for network in ethNetworks:
            comments = None
            try:
                comments = network['comments']
            except KeyError:
                continue

            if(comments):
                comments = comments.strip('\n')
                if(comments == "management"):
                    continue
                bridgesToCheckNames.append(comments)
                bridgesToCheck[comments] = network['iface']
        
        for bridgeToCheck in bridgesToCheckNames:
            foundBridge = False
            for bridgeNetwork in bridgeNetworks:
                bridgeName = bridgeNetwork['iface']
                if(bridgeName == bridgeToCheck):
                    foundBridge = True
                    break

            if(foundBridge):
                print(f":white_check_mark: {bridgeToCheck} exists on host {host}")
            else:
                print(f":x: {bridgeToCheck} not on host {host}")
                print(f"creating {bridgeToCheck} on {host}...")
                proxmoxInstance.nodes(node['node']).network.create(iface=bridgeToCheck, type="bridge", node=node['node'], bridge_vlan_aware=1, autostart=1, bridge_ports=f"{bridgesToCheck[bridgeToCheck]}")

    typer.echo("Callback working!fggg")