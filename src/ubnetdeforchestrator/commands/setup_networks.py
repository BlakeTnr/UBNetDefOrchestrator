import typer
import Proxmox
import proxmoxer
from rich import print

app = typer.Typer()

# Steps
# 1. loop through all nodes
# 2. Read all network adapter, parse out physical adapters with comments & current bridges
# 3. Check for ones bridge adapters that already exist
# 4. Create all adapaters that need to be created, apply

def get_network_adapters(node):
    nodeName = node['node']
    proxmoxInstance = Proxmox.get_proxmox_instance()
    networks = proxmoxInstance.nodes(nodeName).network.get()

    ethWithComments = []
    existingBridges = []
    for network in networks:
        network: dict
        if(network['type'] == "eth" and network.get("comments")):
            ethWithComments.append(network)
        if(network['type'] == "bridge"):
            existingBridges.append(network)

    return [ethWithComments, existingBridges]

def get_adapters_missing_bridges(ethWithComments: list, existingBridges: list):
    adaptersMissingBridges = []
    for eth in ethWithComments:
        bridgeName = eth['comments'].strip("\n")
        if bridgeName not in [existingBridge['iface'] for existingBridge in existingBridges]:
            adaptersMissingBridges.append(eth)

    return adaptersMissingBridges

def vlan_from_bridge_name(bridgeName):
    match bridgeName:
        case "coreblue":
            return 2
        case "corered":
            return 3
        case "io":
            return 4
        case _:
            raise Exception(f"Unkown vlan for {bridgeName}")


def create_missing_bridges(node, adapters_missing_bridges: list):
    proxmoxInstance = Proxmox.get_proxmox_instance()
    nodeName = node['node']

    for adapterMissingBridge in adapters_missing_bridges:
        bridgeName = adapterMissingBridge['comments'].strip("\n")
        slave = adapterMissingBridge['iface']

        if(bridgeName == "management"):
            continue

        vlanID = vlan_from_bridge_name(bridgeName)

        proxmoxInstance.nodes(nodeName).network.create(
            iface=bridgeName,
            type="bridge",
            node=nodeName,
            bridge_vlan_aware=1,
            autostart=1,
            bridge_ports=f"{slave}.{vlanID}"
        )
        print(f":white_check_mark: created {bridgeName} bound to {slave}.{vlanID} on {nodeName}")

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

        ethWithComments, existingBridges = get_network_adapters(node)

        adaptersMissingBridges = get_adapters_missing_bridges(ethWithComments, existingBridges)

        create_missing_bridges(node, adaptersMissingBridges)