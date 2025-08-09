import proxmoxer
import typer

proxmox: proxmoxer.ProxmoxAPI = None

def get_proxmox_instance(host, username, password, realm="pve") -> proxmoxer.ProxmoxAPI:
    global proxmox

    if not proxmox:
        try:
            proxmox = proxmoxer.ProxmoxAPI(host, user=f'{username}@{realm}', password=password, verify_ssl=False)
        except proxmoxer.AuthenticationError:
            print("Username or password were incorrect!")

    return proxmox