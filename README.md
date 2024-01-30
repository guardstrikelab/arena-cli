# Arena-CLI

<b>Official Command Line utility to use Arena in your terminal.</b>

Arena-CLI is designed to extend the functionality of the Arena web application to command line to make the platform more accessible and terminal-friendly to its users.

------------------------------------------------------------------------------------------
## Usage
Set token

```bash
arena set_token [TOKEN]
```

Push the docker image to arena backend

```bash
arena push -t track [IMAGE]:[TAG]
```

## Source Installation

Arena-CLI and its required dependencies can be installed using pip:

   ```sh
   pip install arena
   ```

Once Arena-CLI is installed, check out the [usage documentation](https://cli.eval.ai/).

## Development Setup

1. Setup the development environment for Arena and make sure that it is running perfectly.

2. Clone the arena-cli repository to your machine via git

    ```bash
    git clone https://github.com/guardstrikelab/arena-cli.git arena-cli
    ```

3. Create a virtual environment

    ```bash
    cd arena-cli
    virtualenv -p python3 venv
    source venv/bin/activate
    ```

4. Install the package locally

    ```bash
    pip install -e .
    ```
 
5. Change the arena-cli host to make request to local Arena server running on `http://localhost:8000` by running:
   
   ```bash
   arena host -sh http://localhost:8000
   ```

6. Login to cli using the command ``` arena login```
Two users will be created by default which are listed below -

    ```bash
    Host User - username: host, password: password
    Participant User - username: participant, password: password
    ```

7. Push the docker image to arena backend

   ```bash
   arena push -t track [image]:[tag]
   ```