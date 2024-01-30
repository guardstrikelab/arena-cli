import json
import requests
import sys

from click import echo, style

from arena.config import ARENA_ERROR_CODES
from arena.common import validate_token
from arena.auth import get_request_header, get_host_url


def make_request(path, method, files=None, data=None):
    url = "{}{}".format(get_host_url(), path)
    headers = get_request_header()

    if method == "GET":
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            if response.status_code in ARENA_ERROR_CODES:
                validate_token(response.json())
                echo(
                    style(
                        "\nError: {}\n".format(response.json().get("error")),
                        fg="red",
                        bold=True,
                    )
                )
            else:
                echo(err)
            sys.exit(1)
        except requests.exceptions.RequestException:
            echo(
                style(
                    "\nCould not establish a connection to Arena."
                    " Please check the Host URL.\n",
                    bold=True,
                    fg="red",
                )
            )
            sys.exit(1)
        return response.json()
    elif method == "POST":
        if files:
            files = {"input_file": open(files, "rb")}
        else:
            files = None
        if data is not None:
            data["status"] = "submitting"
        else:
            data = {"status": "submitting"}
        try:
            response = requests.post(
                url, headers=headers, files=files, data=data
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            if response.status_code in ARENA_ERROR_CODES:
                validate_token(response.json())
                echo(
                    style(
                        "\nError: {}\n"
                        "\nUse `arena challenges` to fetch the active challenges.\n"
                        "\nUse `arena challenge CHALLENGE tracks` to fetch the "
                        "active tracks.\n".format(response.json()["error"]),
                        fg="red",
                        bold=True,
                    )
                )
            else:
                echo(err)
            sys.exit(1)
        except requests.exceptions.RequestException:
            echo(
                style(
                    "\nCould not establish a connection to Arena."
                    " Please check the Host URL.\n",
                    bold=True,
                    fg="red",
                )
            )
            sys.exit(1)
        response = json.loads(response.text)
        echo(
            style(
                "\nYour docker file is successfully submitted.\n",
                fg="green",
                bold=True,
            )
        )
        return response
    elif method == "PUT":
        # TODO: Add support for PUT request
        pass
    elif method == "PATCH":
        # TODO: Add support for PATCH request
        pass
    elif method == "DELETE":
        # TODO: Add support for DELETE request
        pass
