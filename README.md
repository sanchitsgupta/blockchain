# Simple Blockchain in Python

[![Build Status](https://travis-ci.org/dvf/blockchain.svg?branch=master)](https://travis-ci.org/dvf/blockchain)

This is a fork of the 'Learn Blockchains by Building One' project by [dvf](https://github.com/dvf). Make sure to check out his [blog post](https://medium.com/p/117428612f46) on the same.

I re-implemented the same functionality for learning purposes. Along the way I made some improvements over the original codebase:

- [x] Use Python 3.10
- [x] Better code structure
- [x] Define Models for Block and Transaction instead of passing them around as raw dictionaries
- [x] Function type-annotations
- [x] Use FastAPI instead of Flask
    - In our case, this mainly helps with easier request-response validation and auto generating the OpenAPI documentation.
- [x] Make endpoints more RESTful
    - For eg. /mine/ endpoint must be a POST operation since it changes the server state.
- [x] Move all business logic to the service layer
    - For eg. mining logic should reside in the Blockchain class instead of the endpoint function.
- [x] Docker-compose file for spinning up multiple nodes at once

## Installation

### 1. Pipenv

1. Make sure [Python 3.10+](https://www.python.org/downloads/) is installed.
2. Install [pipenv](https://github.com/kennethreitz/pipenv).
    ```shell
    $ pip install pipenv
    ```
3. Install requirements
    ```shell
    $ pipenv install
    ```

4. Run some nodes:
    - `$ pipenv run uvicorn src.node_server:app --port 8000`
    - `$ pipenv run uvicorn src.node_server:app --port 8001`

### 2. Docker

Another option for running this program is to use Docker. Follow the instructions below to spawn two nodes.

1. Build the image
    ```shell
    $ docker-compose build
    ```

3. Run 2 nodes
    ```
    $ docker-compose up
    ```

4. To add more nodes, add more services to the [docker-compose.yml](./docker-compose.yml)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
