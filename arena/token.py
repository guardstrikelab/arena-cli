import json
import os

import click
from click import echo, style

from arena.config import AUTH_TOKEN_DIR, AUTH_TOKEN_PATH


@click.group(invoke_without_command=True)
def get_token():
    """
    Get the Arena token.
    """
    if not os.path.exists(AUTH_TOKEN_PATH):
        echo(
            style(
                "\nThe authentication token json file doesn't exist at the required path. "
                "Please download the file from the Profile section of the Arena webapp and "
                "place it at ~/.arena/token.json or use arena -t <token> to add it.\n\n",
                bold=True,
                fg="red",
            )
        )
    else:
        with open(AUTH_TOKEN_PATH, "r") as fr:
            try:
                data = fr.read()
                token_data = json.loads(data)
                echo("Current token is {}".format(token_data["token"]))
            except (OSError, IOError) as e:
                echo(e)


@click.group(invoke_without_command=True)
@click.argument("auth_token")
def set_token(auth_token):
    """
    Configure Arena Token.
    """
    """
    Invoked by `arena set_token <your_arena_auth_token>`.
    """
    if not os.path.exists(AUTH_TOKEN_DIR):
        os.makedirs(AUTH_TOKEN_DIR)
    with open(AUTH_TOKEN_PATH, "w+") as fw:
        try:
            auth_token = {"token": "{}".format(auth_token)}  # noqa
            auth_token = json.dumps(auth_token)
            fw.write(auth_token)
        except (OSError, IOError) as e:
            echo(e)
        echo(
            style(
                "Success: Authentication token is successfully set.",
                bold=True,
                fg="green",
            )
        )
