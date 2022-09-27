import unittest
import blockchain
from unittest.mock import patch


class Blockchain(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self) -> None:
        blockchain.blockchain = []
        return super().tearDown()

    def test_it_can_add_a_value_to_the_block_chain(self):
        blockchain.add_node_to_blockchain(10, None)
        self.assertEqual(blockchain.blockchain, [[None, 10]])

    def test_it_can_output_a_given_blockchain(self):
        blockchain.add_node_to_blockchain(25, blockchain.get_last_blockchain_value())
        blockchain.add_node_to_blockchain(45, blockchain.get_last_blockchain_value())
        self.assertEqual(blockchain.blockchain,  [[None, 25], [[None, 25], 45]])

    def test_user_wants_to_output_the_blockchain_returns_true_if_given_choice_is_2(self):
        self.assertTrue
        (blockchain.user_wants_to_add_a_new_transaction(2))

    def test_user_wants_to_output_the_blockchain_returns_false_if_given_choice_is_not_2(self):
        self.assertFalse
        blockchain.user_wants_to_add_a_new_transaction(None)

    def test_user_wants_to_add_a_new_transaction_returns_true_if_given_choice_is_1(self):
        self.assertTrue
        (blockchain.user_wants_to_add_a_new_transaction(1))

    def test_user_wants_to_add_a_new_transaction_returns_false_if_given_choice_is_not_1(self):
        self.assertFalse
        blockchain.user_wants_to_add_a_new_transaction(None)

    def test_get_user_input_raw_returns_the_input(self):
        blockchain.get_user_input("Msg")
    # get_input will return 'yes' during this test

    @patch('blockchain.', return_value='yes')
    def test_answer_yes(self, input):
        self.assertEqual(blockchain.grouped_transaction(blockchain.blockchain), 'you entered yes')


if __name__ == '__main__':
    unittest.main()
