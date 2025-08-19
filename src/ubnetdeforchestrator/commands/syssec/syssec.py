import typer
from commands.syssec import teardown
from commands.syssec import setup
from commands.syssec import load_students
from commands.syssec import deploy_vm

app = typer.Typer()

app.add_typer(setup.app, name="setup")
app.add_typer(teardown.app, name="teardown")
app.add_typer(load_students.app, name="loadstudents")
app.add_typer(deploy_vm.app, name="deployvm")