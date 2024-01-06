import logging
import os

import typer
from rich.logging import RichHandler

from spatle.server import WebServer
from spatle.game import Game

app = typer.Typer()


@app.callback()
def main(context: typer.Context):
    debug = os.getenv("SPATLE_DEBUG", None)
    logging.basicConfig(
        format="%(message)s",
        level=logging.DEBUG if debug else logging.INFO,
        handlers=[RichHandler(rich_tracebacks=True, tracebacks_suppress=[typer])],
    )
    logging.getLogger("asyncio").setLevel(logging.ERROR)
    print("SPATLE: Speech PAThology wordLE!\n")
    if not context.invoked_subcommand:
        return play(context)


@app.command()
def play(context: typer.Context):
    game = Game()
    while game.guesses_remaining:
        if game.guess(typer.prompt(f"\n{game}\nEnter your five-letter guess (CTRL+C to quit)")):
            print(f"Correct! The solution was: {game.solution}")
            return
    print(f"You are out of guesses! The solution was: {game.solution}")


@app.command()
def server(
    context: typer.Context,
    host: str = typer.Argument(
        "0.0.0.0",
        help="bind address",
    ),
    port: int = typer.Argument(
        2323,
        help="bind port",
    ),
    debug: bool = typer.Option(False, help="Enable debugging output"),
):
    """
    Start the Spatle webserver.
    """
    WebServer(host=host, port=port, debug=debug).start()


if __name__ == "__main__":
    app()
