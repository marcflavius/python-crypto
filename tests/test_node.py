import unittest
from unittest.mock import MagicMock, patch
from node import Node
from log import Log
from transaction import Transaction
from blockchain import Blockchain
from tests.mock_utils import generate_single_transaction


class TestNode(unittest.TestCase):
    @patch.object(Blockchain, "load_blockchain")
    @patch.object(Node, "controller")
    @patch.object(Log, "log")
    def test_main(self, load_blockchain, controller, logger):
        blockchain = Blockchain("Marc")
        node = Node(blockchain, blockchain.owner)
        node.main()
        blockchain.blockchain = []
        blockchain.open_transaction = [Transaction(generate_single_transaction())]
        assert load_blockchain.called
        assert controller.called
        assert logger.called
        logger.log.called_with("Good Bye!")
        self.assertEqual(blockchain.blockchain, [])

    @patch.object(Node, "get_user_choice", side_effect=[("1", [1]), ("q", ["q"])])
    @patch.object(Node, "get_user_transaction", side_effect=[(10, "Bob")])
    def test_controller_add_transaction_success(
        self,
        get_user_choice,
        get_user_transaction,
    ):
        blockchain = Blockchain("Marc")
        node = Node(blockchain, blockchain.owner)
        node.controller()
        assert get_user_choice.called
        assert get_user_transaction.called

    @patch.object(Node, "get_user_choice", side_effect=[("3", [3]), ("q", ["q"])])
    @patch.object(Node, "user_wants_to_mind_new_block", return_value=True)
    def test_controller_mine_block_success(
        self,
        get_user_choice,
        user_wants_to_mind_new_block,
    ):
        blockchain = Blockchain("Marc", [], [])
        node = Node(blockchain, blockchain.owner)
        node.blockchain.mine_block = MagicMock(return_value=None)
        node.controller()
        get_user_choice.assert_called_once_with("3")
        user_wants_to_mind_new_block.assert_called()

    def test_user_wants_to_add_a_new_transaction(self):
        self.assertTrue(Node.user_wants_to_add_a_new_transaction(1))

    def test_user_wants_to_output_the_blockchain(self):
        self.assertTrue(Node.user_wants_to_output_the_blockchain(2))

    def test_user_wants_to_mind_new_block(self):
        self.assertTrue(Node.user_wants_to_mind_new_block(3))

    def test_user_wants_to_output_participants(self):
        self.assertTrue(Node.user_wants_to_output_participants(4))

    def test_user_wants_to_output_the_blockchain_falsy(self):
        self.assertFalse(Node.user_wants_to_add_a_new_transaction(None))

    def test_user_wants_to_add_a_new_transaction_falsy(self):
        self.assertFalse(Node.user_wants_to_add_a_new_transaction(None))
