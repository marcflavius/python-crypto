import pprint
import unittest
import blockchain


class Blockchain(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self) -> None:
        blockchain.blockchain = []
        return super().tearDown()

    @unittest.skip
    def test_it_can_add_a_transaction_to_the_open_transaction_queue(self):
        blockchain.add_transaction(recipient="Bob", sender="Marc", amount=10,)
        self.assertEqual(blockchain.open_transaction, [{'amount': 10, 'recipient': 'Bob', 'sender': 'Marc'}])

    # def test_it_can_output_a_given_blockchain(self):
    #     blockchain.add_transaction(25, blockchain.get_last_blockchain_value())
    #     blockchain.add_transaction(45, blockchain.get_last_blockchain_value())
    #     self.assertEqual(blockchain.blockchain,  [[None, 25], [[None, 25], 45]])

    @unittest.skip
    def test_user_wants_to_output_the_blockchain_returns_true_if_given_choice_is_2(self):
        self.assertTrue
        (blockchain.user_wants_to_add_a_new_transaction(2))

    @unittest.skip
    def test_user_wants_to_output_the_blockchain_returns_false_if_given_choice_is_not_2(self):
        self.assertFalse
        blockchain.user_wants_to_add_a_new_transaction(None)

    @unittest.skip
    def test_user_wants_to_add_a_new_transaction_returns_true_if_given_choice_is_1(self):
        self.assertTrue
        (blockchain.user_wants_to_add_a_new_transaction(1))

    @unittest.skip
    def test_user_wants_to_add_a_new_transaction_returns_false_if_given_choice_is_not_1(self):
        self.assertFalse
        blockchain.user_wants_to_add_a_new_transaction(None)

    @unittest.skip
    def test_blockchain_is_valid(self):
        blockchain.add_transaction(recipient="Bob", sender="Marc", amount=10)
        blockchain.mine_block()
        is_valid = blockchain.verify_chain()
        self.assertTrue(is_valid)
    
    
    # @unittest.skip
    def test_blockchain_is_invalid(self):
        blockchain.add_transaction(recipient="Bob", sender="Marc", amount=10)
        blockchain.mine_block()
        blockchain.add_transaction(recipient="Test", sender="Marc", amount=10)
        blockchain.mine_block()
        
        is_valid = blockchain.verify_chain()
        self.assertTrue(is_valid)


    @unittest.skip
    def test_test(self):
        a = []
        dic = {"test":"insert",}
        a.append(dic)
        print(dic["test"])
        print(a)

    
if __name__ == '__main__':
    unittest.main()
