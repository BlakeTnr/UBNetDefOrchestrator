import typer
from commands.syssec import teardown
from commands.syssec import setup
from commands.syssec import load_students

app = typer.Typer()

app.add_typer(setup.app, name="setup")
app.add_typer(teardown.app, name="teardown")
app.add_typer(load_students.app, name="loadstudents")