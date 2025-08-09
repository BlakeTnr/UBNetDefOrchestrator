import typer
from commands.syssec import teardown

app = typer.Typer()

app.add_typer(teardown.app, name="teardown")