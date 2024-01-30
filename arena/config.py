import os

from os.path import expanduser


AUTH_TOKEN_FILE_NAME = "token.json"

HOST_URL_FILE_NAME = "host_url"

AUTH_TOKEN_DIR = expanduser("~/.arena/")

AUTH_TOKEN_PATH = os.path.join(AUTH_TOKEN_DIR, AUTH_TOKEN_FILE_NAME)

API_HOST_URL = os.environ.get("ARENA_API_URL", "https://52.83.27.237")

ARENA_ERROR_CODES = [400, 401, 403, 406]

HOST_URL_FILE_PATH = os.path.join(AUTH_TOKEN_DIR, HOST_URL_FILE_NAME)

ENVIRONMENT = os.environ.get("ARENA_CLI_ENVIRONMENT", "PRODUCTION")

LOCAL_DOCKER_REGISTRY_URI = os.environ.get(
    "ARENA_LOCAL_DOCKER_REGISTRY_URI", "localhost:5000"
)

AWS_REGION = os.environ.get("AWS_REGION_NAME", "us-west-1")
