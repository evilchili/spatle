import logging
import os

import typer
from rich.logging import RichHandler

from spatle.server import WebServer

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
    WebServer.start(host=host, port=port, debug=debug)


if __name__ == "__main__":
    app()
