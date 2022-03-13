from urllib.parse import urlparse

from fastapi import FastAPI, Request, HTTPException

from .blockchain import Blockchain
from .schemas import BaseResponse, Block, GetChainResponse, Transaction, NodesList
from .utils import get_new_node_identifier


node_identity = get_new_node_identifier()
blockchain = Blockchain(node_identity)
app = FastAPI(title="Simple Blockchain in Python")


@app.post('/mine/', response_model=Block, status_code=201)
def mine_block():
    """ Instructs the node to mine a block """

    return blockchain.mine_block()


@app.post('/transaction/', response_model=BaseResponse, status_code=201)
def add_transaction(transaction: Transaction):
    """ Instructs the node to add the transaction to its list of current transactions """

    index = blockchain.add_transaction(transaction)
    return {'message': f'Transaction will be added to the next mined block (index:{index})'}


@app.get('/chain/', response_model=GetChainResponse)
def get_chain():
    """ Returns the node's blockchain """

    return {'chain': blockchain.chain}


@app.post('/nodes/', response_model=BaseResponse, status_code=201)
def register_nodes(data: NodesList, request: Request):
    """ Instructs the node to register given node addresses """

    # clients can not register our own url
    parsed_url = urlparse(request.url._url)
    server_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    if server_url in data.nodes:
        raise HTTPException(
            status_code=422,
            detail=f'My own address ({server_url}) detected in the provided list of addresses'
        )

    blockchain.register_nodes(data.nodes)
    return {'message': 'New nodes have been registered'}


@app.post('/resolve-conflicts/', response_model=BaseResponse, status_code=201)
def resolve_conflicts():
    """ Instructs the node to replace its chain with the authoritative chain """

    replaced = blockchain.resolve_conflicts()
    msg = 'Our chain was replaced' if replaced else 'Our chain is authoritative'
    return {'message': msg}
