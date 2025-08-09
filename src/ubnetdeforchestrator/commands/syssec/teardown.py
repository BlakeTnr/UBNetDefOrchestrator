import typer
import Proxmox
import proxmoxer
from rich import print
from rich.prompt import Confirm
import sys

app = typer.Typer()

@app.callback(invoke_without_command=True)
def teardown_callback(host, username, password, realm="pve"):
    confirmed = Confirm.ask(":warning:  This is irreversible! This will delete all of syssec. Are you sure?")
    if not confirmed:
        print("Cancelled")
        sys.quit()
    
    print("continue")