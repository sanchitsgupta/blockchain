from unittest import TestCase

from fastapi.testclient import TestClient

from src.schemas import Transaction
from src.node_server import app, blockchain


class TestAPIEndpoints(TestCase):
    """
    Testing the API endpoints response and their behaviour.
    Helps in good coverage with less number of tests.
    """

    def setUp(self):
        self.client = TestClient(app)

    def add_dummy_transaction(self, sender='a', recipient='b', amount=5.0):
        transaction = Transaction(sender=sender, recipient=recipient, amount=amount)
        blockchain.add_transaction(transaction)

    def test_add_transaction(self):
        transaction = Transaction(sender='a', recipient='b', amount=5.0)
        response = self.client.post("/transaction/", json=transaction.dict())

        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(
            response.json(),
            {'message': f'Transaction will be added to the next mined block (index:1)'}
        )
        self.assertEqual(blockchain.curr_transactions[-1], transaction)

    def test_mine_block(self):
        self.add_dummy_transaction()
        response = self.client.post("/mine/")

        self.assertEqual(response.status_code, 201)
        for key in ['index', 'timestamp', 'transactions', 'proof', 'previous_hash']:
            assert key in response.json()

        self.assertEqual(len(blockchain.chain), 2)
        self.assertEqual(len(blockchain.curr_transactions), 0)

    def test_get_blockchain(self):
        response = self.client.get("/chain/")
        res_dict = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(res_dict['chain']), 1)

    def test_register_nodes(self):
        data = {'nodes': ['http://192.168.1.1:3000', 'http://192.168.0.5:5000']}
        response = self.client.post("/nodes/", json=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(blockchain.nodes), 2)
        assert isinstance(next(iter(blockchain.nodes)), str)

    def test_register_invalid_nodes(self):
        data = {'nodes': ['http://testserver', 'http://192.168.0.5:5000']}
        response = self.client.post("/nodes/", json=data)
        self.assertEqual(response.status_code, 422)
