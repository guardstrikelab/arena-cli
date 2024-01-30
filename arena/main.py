import click
from click import echo
from arena.submission import push
from arena.token import get_token, set_token
from arena.login import login
from arena.set_host import host


@click.version_option()
@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    """
    Welcome to the Arena CLI.
    """
    if ctx.invoked_subcommand is None:
        welcome_text = (
            """
                          ###    #######  #######  ##   ##    ###  
                         #####   ##   ##  ##       ###  ##   ##### 
                        ##   ##  ######   #####    ## # ##  ##   ##
                        #######  ##  ##   ##       ##  ###  #######
                        ##   ##  ##   ##  #######  ##   ##  ##   ## \n\n
                        """
            "Welcome to the Arena CLI. Use arena --help for viewing all the options\n"
            "CHALLENGE and TRACK placeholders used throughout the CLI are"
            " for challenge_id\nand track_id of the challenges and tracks."
        )
        echo(welcome_text)
    # latest_version = get_latest_version()
    # if __version__ < latest_version:
    #     echo(
    #         style(
    #             "\nUpdate:\n"
    #             "\nPlease install the latest version of Arena-CLI!\n",
    #             "\nUse: pip install --upgrade arena\n",
    #             fg="red",
    #             bold=True,
    #         )
    #     )
    #     sys.exit(1)


main.add_command(push)
main.add_command(get_token)
main.add_command(set_token)
main.add_command(login)
main.add_command(host)
