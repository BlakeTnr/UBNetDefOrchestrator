import typer
from commands.syssec import teardown
from commands.syssec import setup

app = typer.Typer()

app.add_typer(setup.app, name="setup")
app.add_typer(teardown.app, name="teardown")