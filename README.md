# Simple Blockchain in Python

[![build](https://github.com/sanchitsgupta/blockchain/actions/workflows/ci.yml/badge.svg)](https://github.com/sanchitsgupta/blockchain/actions/workflows/ci.yml)
![PyPI pyversions](https://img.shields.io/github/pipenv/locked/python-version/sanchitsgupta/blockchain)
![Linux](https://svgshare.com/i/Zhy.svg)
![PyPI license](https://img.shields.io/github/license/sanchitsgupta/blockchain)


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

## Testing

Tests can be run using pytest:
```shell
$ pipenv run pytest --cov=src
```

## Potential Improvements

I made a note of some core blockchain features that are missing from this implementation. Interested readers can try working on these for a better understanding.

- Nodes using Public Key Infrastructure (such as for signing their transactions)
- Transaction Validation (person sending coins has the said amount or not?)
- Transaction Queuing (miners can work on transactions with a good payoff; at the same time the chain must make sure that no transactions starve)
- P2P communication between nodes
- Proof-of-Work Verification
- Mining difficulty proportional to remaining number of coins and the network's hash rate.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
