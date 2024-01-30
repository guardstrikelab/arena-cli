import os

import base64
import boto3
import click
import docker
import json
import shutil
import sys
import tempfile
import uuid


from arena.common import notify_user
from arena.request import make_request
from arena.urls import URLS
from arena.config import (
    ENVIRONMENT,
    AWS_REGION,
    LOCAL_DOCKER_REGISTRY_URI,
)


@click.command()
@click.argument("IMAGE", nargs=1)
@click.option(
    "-t",
    "--track",
    help="challenge-track-name to which image is to be pushed",
    required=True,
)
# Dependency Injection for Local Registry URI for Dev and Test environment
@click.option(
    "-u",
    "--url",
    help="Docker Registry URI where image will be pushed",
    required=False,
    default=LOCAL_DOCKER_REGISTRY_URI,
)
@click.option("--public", is_flag=True)
@click.option("--private", is_flag=True)
def push(image, track, url, public, private):
    """
    Push docker image to a particular challenge track.
    """
    """
    Invoked by `arena push IMAGE:TAG -t TRACK_ID`.
    """
    if len(image.split(":")) != 2:
        message = "\nError: Please enter the tag name with image.\n\nFor eg: `arena push ubuntu:latest --track 123`"
        notify_user(message, color="red")
        sys.exit(1)

    if public and private:
        message = "\nError: Submission can't be public and private.\nPlease select either --public or --private"
        notify_user(message, color="red")
        sys.exit(1)

    submission_metadata = {}
    if public:
        submission_metadata["is_public"] = json.dumps(True)
    elif private:
        submission_metadata["is_public"] = json.dumps(False)

    tag = str(uuid.uuid4())
    docker_client = docker.from_env()
    try:
        docker_image = docker_client.images.get(image)
    except docker.errors.ImageNotFound:
        message = "\nError: Image not found. Please enter the correct image name and tag."
        notify_user(message, color="red")
        sys.exit(1)

    request_path = URLS.phase_details_using_slug.value
    request_path = request_path.format(track)
    response = make_request(request_path, "GET")
    challenge_pk = response.get("challenge")
    phase_pk = response.get("id")

    request_path = URLS.challenge_details.value
    request_path = request_path.format(challenge_pk)
    response = make_request(request_path, "GET")
    max_docker_image_size = response.get("max_docker_image_size")

    docker_image_size = docker_image.__dict__.get("attrs").get("VirtualSize")
    if docker_image_size > max_docker_image_size:
        max_docker_image_size = convert_bytes_to(max_docker_image_size, "gb")
        message = "\nError: Image is too large. The maximum image size allowed is {} GB".format(
            max_docker_image_size
        )
        notify_user(message, color="red")
        sys.exit(1)

    request_path = URLS.get_aws_credentials.value
    request_path = request_path.format(phase_pk)

    response = make_request(request_path, "GET")
    federated_user = response["success"]["federated_user"]
    repository_uri = response["success"]["docker_repository_uri"]

    # Production Environment
    if ENVIRONMENT == "PRODUCTION":
        AWS_ACCOUNT_ID = federated_user["FederatedUser"][
            "FederatedUserId"
        ].split(":")[0]
        AWS_SERVER_PUBLIC_KEY = federated_user["Credentials"]["AccessKeyId"]
        AWS_SERVER_SECRET_KEY = federated_user["Credentials"][
            "SecretAccessKey"
        ]
        SESSION_TOKEN = federated_user["Credentials"]["SessionToken"]

        ecr_client = boto3.client(
            "ecr",
            region_name=AWS_REGION,
            aws_access_key_id=AWS_SERVER_PUBLIC_KEY,
            aws_secret_access_key=AWS_SERVER_SECRET_KEY,
            aws_session_token=SESSION_TOKEN,
        )

        token = ecr_client.get_authorization_token(
            registryIds=[AWS_ACCOUNT_ID]
        )
        ecr_client = boto3.client("ecr", region_name=AWS_REGION)
        username, password = (
            base64.b64decode(
                token["authorizationData"][0]["authorizationToken"]
            )
            .decode()
            .split(":")
        )
        registry = token["authorizationData"][0]["proxyEndpoint"]
        docker_client.login(
            username, password, registry=registry, dockercfg_path=os.getcwd()
        )

    # Development and Test Environment
    else:
        repository_uri = "{0}/{1}".format(url, repository_uri.split("/")[1])

    # Tag and push docker image and create a submission if successfully pushed
    docker_client.images.get(image).tag("{}:{}".format(repository_uri, tag))
    for line in docker_client.images.push(
        repository_uri, tag, stream=True, decode=True
    ):
        if line.get("status") in ["Pushing", "Pushed"] and line.get(
            "progress"
        ):
            print("{id}: {status} {progress}".format(**line))
        elif line.get("errorDetail"):
            error = line.get("error")
            notify_user(error, color="red")
        elif line.get("aux"):
            aux = line.get("aux")
            pushed_image_tag = aux["Tag"]
            submitted_image_uri = "{}:{}".format(
                repository_uri, pushed_image_tag
            )
            BASE_TEMP_DIR = tempfile.mkdtemp()
            data = {"submitted_image_uri": submitted_image_uri}
            submission_file_path = os.path.join(
                BASE_TEMP_DIR, "submission.json"
            )
            with open(submission_file_path, "w") as outfile:
                json.dump(data, outfile)
            request_path = URLS.make_submission.value
            request_path = request_path.format(challenge_pk, phase_pk)
            response = make_request(request_path, "POST", submission_file_path, data=submission_metadata)
            shutil.rmtree(BASE_TEMP_DIR)
        else:
            print(
                " ".join(
                    "{}: {}".format(k, v)
                    for k, v in line.items()
                    if k != "progressDetail"
                )
            )


def convert_bytes_to(byte, to, bsize=1024):
    """
    Convert bytes to KB, MB, GB etc.
    Arguments:
        bytes {int} -- The bytes which are to be converted
        to {str} -- To which unit it is to be converted
    """
    units_mapping = {"kb": 1, "mb": 2, "gb": 3, "tb": 4, "pb": 5, "eb": 6}
    unit = byte
    for value in range(units_mapping[to]):
        unit = int(unit / bsize)

    return unit
