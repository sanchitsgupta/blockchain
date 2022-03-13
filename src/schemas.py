"""
Object schemas (such as the Block schema) are defined here as Pydantic models
"""

import hashlib

from pydantic import BaseModel, AnyHttpUrl, conset


class Transaction(BaseModel):
    sender: str
    recipient: str
    amount: float


class Block(BaseModel):
    index: int
    timestamp: float
    transactions: list[Transaction]
    proof: int
    previous_hash: str

    def hash(self) -> str:
        """
        Returns SHA-256 hash of the block

        :return: Hash of the block
        """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = self.json(sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()


class BaseResponse(BaseModel):
    message: str


class GetChainResponse(BaseModel):
    chain: list[Block]


class NodesList(BaseModel):
    nodes: conset(AnyHttpUrl, min_items=1)
