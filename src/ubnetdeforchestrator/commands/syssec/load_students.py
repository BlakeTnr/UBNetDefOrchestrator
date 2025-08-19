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
from mattermostdriver import Driver
from mattermostdriver.exceptions import ResourceNotFound

app = typer.Typer()

@app.callback(invoke_without_command=True)
def load_students_callback(host, username, password, csvpath, mattermosturl, mattermostusername, mattermostpassword, realm="pve"):
    infra = ProxmoxInfra(host, username, password, realm)
    
    teamStudentMappings = process_team_csv(csvpath)
    
    for teamStudentMapping in teamStudentMappings:
        print(teamStudentMapping)
        team = teamStudentMapping[0]
        student = teamStudentMapping[1]
        password = generate_password()
        infra.createStudent(student, password)
        _notify_student(mattermosturl, mattermostusername, mattermostpassword, student, password)
        
        infra.assignStudentToTeam(student, team)

def _notify_student(mattermostUrl, mattermostUsername, mattermostPassword, student: Student, studentPassword):
    mattermost = Driver({
        'url': mattermostUrl,
        'login_id': mattermostUsername,
        'password': mattermostPassword,
        'scheme': 'https',
        'port': 443,
        'basepath': '/api/v4',
        'verify': False
    })
    mattermost.login()

    channel = None
    try:
        channel = _get_dm_channel(mattermost, student.identifier)
    except ResourceNotFound:
        channel  = _create_dm_channel(mattermost, student)
    _send_notification_message(mattermost, channel['id'], student.identifier, studentPassword)

def _create_dm_channel(mattermost, student):
    self = mattermost.users.get_user(user_id='me')
    studentMattermost = mattermost.users.get_user_by_username(student.identifier)

    channel = mattermost.channels.create_direct_message_channel([studentMattermost['id'], self['id']])
    return channel
    
def _send_notification_message(mattermost, channelID, username, password):
    mattermost.posts.create_post(options={
    'channel_id': channelID,
    'message': f"Hello, your new username for cdr-vm.cse.buffalo.edu is '{username}' and your password is '{password}'"
    })

def _get_dm_channel(mattermost, otherPerson):
    ubnetdef = mattermost.teams.get_team_by_name("UBNetDef") # mx69rrsampf6dgapamukm4w5by
    ownUser = mattermost.users.get_user(user_id='me') # dbu6zcu4s3dj9g6k6e49xhuigh
    otherUser = mattermost.users.get_user_by_username(otherPerson)
    try:
        channel = mattermost.channels.get_channel_by_name(ubnetdef['id'], f"{otherUser['id']}__{ownUser['id']}")
        return channel
    except ResourceNotFound:
        channel = mattermost.channels.get_channel_by_name(ubnetdef['id'], f"{ownUser['id']}__{otherUser['id']}")
        return channel

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
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))