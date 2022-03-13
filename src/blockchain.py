import hashlib
from time import time
from timeit import default_timer

import requests

from .schemas import Block, Transaction


class Blockchain:
    """
    Blockchain class that is responsible for managing the chain.
    It handles tasks such as creating new blocks, adding new transactions, resolving conflicts etc.

    Each node will have its own local copy of the blockchain.
    """

    def __init__(self, node_identifier: str):
        self.node_identifier: str = node_identifier

        self.chain: list[Block] = []
        self.curr_transactions: list[Transaction] = []
        self.nodes: set[str] = set()

        # Add the genesis block to the chain
        self.chain.append(
            Block(index=0, timestamp=time(), transactions=[], proof=100, previous_hash='0')
        )

    @property
    def last_block(self) -> Block:
        return self.chain[-1]

    def register_nodes(self, addresses: list[str]) -> None:
        """
        Add the list of node addresses to this node's data.
        For communication, a node must maintain the list of other nodes in the network.

        :param address: Address of node. Eg. 'http://192.168.0.5:5000'
        """

        for address in addresses:
            self.nodes.add(str(address))

    def add_transaction(self, transaction: Transaction) -> int:
        """
        Adds the transaction to the list of current transactions.
        It will get added to the next mined block.

        :param transaction: Transaction
        :return: The index of the Block that will hold this transaction
        """

        # NOTE: Ideally, a node will validate the transaction before adding it
        # For simplicity we have skipped transaction validation

        self.curr_transactions.append(transaction)
        return self.last_block.index + 1

    def compute_proof(self) -> int:
        """
        Simple Proof of Work Algorithm:
        - Find a number p' such that hash(pp'h) contains leading 4 zeroes
        - Where p is the previous proof, and p' is the new proof, h is the last block's hash

        :param last_block: Last Block
        :return: Proof
        """

        start_t = default_timer()
        last_proof = self.last_block.proof
        last_hash = self.last_block.hash()

        proof = 0
        while not self.is_valid_proof(last_proof, proof, last_hash):
            proof += 1

        print(f'Proof of Work took {default_timer() - start_t} secs.')
        return proof

    @staticmethod
    def is_valid_proof(last_proof: int, proof: int, last_hash: str) -> bool:
        """
        Validates the Proof

        :param last_proof: Previous Proof
        :param proof: Current Proof
        :param last_hash: The hash of the Previous Block
        :return: True if correct, False if not.
        """

        guess = f'{last_proof}{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def create_block(self, proof: int) -> Block:
        """
        Create a new Block and add it to the chain

        :param proof: The proof given by the Proof of Work algorithm
        :param previous_hash: Hash of previous Block
        :return: New Block
        """

        block = Block(
            index=len(self.chain) + 1,
            timestamp=time(),
            transactions=self.curr_transactions,
            proof=proof,
            previous_hash=self.last_block.hash(),
        )

        # Reset the current list of transactions
        self.curr_transactions = []
        return block

    def mine_block(self) -> Block:
        """
        Mine a block and add it to the chain

        In real scenarios, mining will happen when the current_transactions list has reached its limit
        For example, Bitcoin chain has a limit of 1MB per block.

        But for simplicity, we will do it on demand

        :return: Forged Block
        """

        # We run the proof of work algorithm to get the next proof
        proof = self.compute_proof()

        # NOTE: After proof computation, we'll need to broadcast it to other nodes for verification
        # for simplicity, we'll skip the above step and assume the proof is valid

        # For our work, we reward ourselves with 1 coin. Ideally, some other node will add this transaction
        self.add_transaction(
            Transaction(sender="0", recipient=self.node_identifier, amount=1.0)     # "0" signifies the chain
        )

        # create and add the block to the chain
        block = self.create_block(proof)
        self.chain.append(block)
        return block

    def is_valid_chain(self, chain: list[Block]) -> bool:
        """
        Check if a given blockchain is valid

        :param chain: A blockchain
        :return: True if valid, False if not
        """

        for idx in range(1, len(chain)):
            prev_block = chain[idx - 1]
            curr_block = chain[idx]

            prev_block_hash = prev_block.hash()
            if curr_block.previous_hash != prev_block_hash:
                return False

            if not self.is_valid_proof(prev_block.proof, curr_block.proof, prev_block_hash):
                return False

        return True

    @staticmethod
    def parse_chain_dict(chain: dict) -> list[Block]:
        return [Block(**block) for block in chain]

    def resolve_conflicts(self) -> bool:
        """
        This is our consensus algorithm, it resolves conflicts
        by replacing our chain with the longest valid one in the network.

        :return: True if our chain was replaced, False if not
        """

        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in self.nodes:
            response = requests.get(f'{node}/chain/')

            if response.status_code == 200:
                chain = self.parse_chain_dict(response.json()['chain'])

                # Check if the length is longer and the chain is valid
                if len(chain) > max_length and self.is_valid_chain(chain):
                    max_length = len(chain)
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False
