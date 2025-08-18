import string
import typer
import Proxmox
import proxmoxer
from rich import print
from rich.prompt import Confirm
import sys
from syssec.Student import Student
from syssec.Team import Team
from ubnetdeforchestrator.ProxmoxInfra import ProxmoxInfra
import pandas as pd
import secrets

app = typer.Typer()

@app.callback(invoke_without_command=True)
def load_students_callback(host, username, password, csvPath, realm="pve"):
    infra = ProxmoxInfra(host, username, password, realm)
    
    teamStudentMappings = process_team_csv(csvPath)
    
    for teamStudentMapping in teamStudentMappings:
        team = teamStudentMapping[0]
        student = teamStudentMapping[1]
        infra.createStudent(student)
        infra.assignStudentToTeam(student, team)

def process_team_csv(csv_path: str) -> list[int, Student]:
    """
    Reads a CSV file, checks for 'team_number' and 'UBIT' columns,
    and returns a list of [team_number, Student(ubit)] pairs.
    """
    df = pd.read_csv(csv_path)

    required_columns = {"team_number", "UBIT"}
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    # Build list of [team_number, Student(ubit)]
    return [[Team(row.team_number), Student(row.UBIT)] for row in df.itertuples(index=False)]

def generate_password(length=12):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))