import typer


app = typer.Typer()


@app.callback()
def main():
    """Mine repositories for maintenance and evolution signals."""
