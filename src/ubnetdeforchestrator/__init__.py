from proxmoxer import ProxmoxAPI
import proxmoxer
import typer

def main(host: str, username, password, realm = "pve"):
    try:
        proxmox = ProxmoxAPI(host, user=f'{username}@{realm}', password=password, verify_ssl=False)
    except proxmoxer.AuthenticationError:
        print("Username or password were incorrect!")

if __name__ == "__main__":
    typer.run(main)