import typer

app = typer.Typer()

@app.callback(invoke_without_command=True)
def test_callback():
    typer.echo("Callback working!")

@app.command()
def default():
    typer.echo("Working!")