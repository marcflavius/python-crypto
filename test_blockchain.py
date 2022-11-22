import unittest
from unittest.mock import patch
import blockchain

genesis_block = {
    "previous_hash": "GENESIS_BLOCK",
    "index": 0,
    "transactions": [],
    "salt": 22,
}
derived_from_genesis_block = {
    "previous_hash": "0cdfe6d341443fb03e149add1696d83da65e8ca9ed7a19e28cda0212c45dbf89",
    "index": 1,
    "transactions": [],
    "salt": 11,
}
falsy_derivation_of_genesis_block = {
    "previous_hash": "0cdfe6d341443fb03e149add1696d83da65e8ca9ed7a19e28cda0212c45dbf89",
    "index": 1,
    "transactions": [],
    "salt": 22,
}


class Blockchain(unittest.TestCase):
    def setUp(self):
        blockchain.blockchain = []
        blockchain.open_transaction = []
        blockchain.owner = "Marc"
        blockchain.participants = set({"Marc"})
        blockchain.genesis_block = genesis_block
        return super().tearDown()

    def tearDown(self) -> None:
        return super().tearDown()

    # (start)
    @patch(
        "blockchain.get_last_blockchain_value", side_effect=[derived_from_genesis_block]
    )
    @patch(
        "blockchain.hash_block",
        side_effect=[
            "0412a7b5869a471587e0fa102ad717055fbcde7e2fd2c22c03f0590f71f71b96"
        ],
    )
    @patch("blockchain.verify_chain", side_effect=[True, True])
    @patch("blockchain.logger")
    def test_mind_block_success(
        self, get_last_blockchain_value, hash_block, verify_chain, logger
    ):
        given_blockchain = [genesis_block, derived_from_genesis_block]
        open_transaction = []
        blockchain.mine_block(given_blockchain, open_transaction)
        self.assertEqual(len(given_blockchain), 3)
        self.assertEqual(given_blockchain[2]["index"], 2)
        self.assertEqual(given_blockchain[2]["index"], 2)
        get_last_blockchain_value.called
        hash_block.called
        verify_chain.called
        logger.called
        blockchain.logger.assert_called_with("Block added!")

    @patch(
        "blockchain.get_last_blockchain_value", side_effect=[derived_from_genesis_block]
    )
    @patch(
        "blockchain.hash_block",
        side_effect=[
            "0412a7b5869a471587e0fa102ad717055fbcde7e2fd2c22c03f0590f71f71b96"
        ],
    )
    @patch("blockchain.verify_chain", side_effect=[False])
    @patch("blockchain.logger")
    def test_mind_block_fails(
        self, get_last_blockchain_value, hash_block, verify_chain, logger
    ):
        given_blockchain = [genesis_block, falsy_derivation_of_genesis_block]
        init_blockchain = given_blockchain[:]
        open_transaction = []
        blockchain.mine_block(given_blockchain, open_transaction)
        self.assertEqual(len(given_blockchain), 3)
        self.assertEqual(given_blockchain[2]["index"], 2)
        self.assertEqual(given_blockchain[2]["index"], 2)
        get_last_blockchain_value.called
        hash_block.called
        verify_chain.called
        logger.called
        blockchain.get_last_blockchain_value.called_with(init_blockchain)
        blockchain.logger.called_with("Invalid chain!")

    @patch("blockchain.find_block_salt", return_value=22)
    def test_verify_the_chain_with_one_block(self, find_block_salt):
        blockchain.blockchain = [genesis_block]
        valid = blockchain.verify_chain(blockchain.blockchain)
        self.assertEqual(valid, True)
        find_block_salt.called

    def test_verify_the_chain_with_multi_block_fail(self):
        blockchain.blockchain = [genesis_block, genesis_block]
        valid = blockchain.verify_chain(blockchain.blockchain)
        self.assertEqual(valid, False)

    @patch("blockchain._blockchain_has_zero_or_one_block", return_value=False)
    @patch("blockchain._is_first_block", side_effect=[True, False])
    @patch(
    "blockchain.hash_block",
    return_value="0cdfe6d341443fb03e149add1696d83da65e8ca9ed7a19e28cda0212c45dbf89",
    )
    def test_verify_the_chain_with_multi_block(
        self,
        _blockchain_has_zero_or_one_block,
        _is_first_block,
         hash_block,
    ):
        stub_blockchain = [genesis_block, derived_from_genesis_block]
        init_stub_blockchain = stub_blockchain[:]
        valid = blockchain.verify_chain(stub_blockchain)
        self.assertEqual(valid, True)
        assert _blockchain_has_zero_or_one_block.called
        blockchain._blockchain_has_zero_or_one_block.assert_called_with(
            init_stub_blockchain
        )
        assert _is_first_block.called
        assert hash_block.called
        blockchain._is_first_block.assert_called_with(1)

    @patch(
        "blockchain.get_last_blockchain_value",
        return_value={
            "previous_hash": "076f74c1e78bceb14a65775013948f24eaacc3ac1bc7e3e911fe4aa3ae198c7"
        },
    )
    def test_valid_salt(self, get_last_blockchain_value):
        open_transaction = [{"sender": "Marc", "recipient": "Bob", "amount": 100}]
        previous_hash = blockchain.get_last_blockchain_value()["previous_hash"]
        salt = blockchain.find_block_salt(open_transaction, previous_hash)
        valid = blockchain.valid_salt(open_transaction, previous_hash, 19)
        get_last_blockchain_value.called
        self.assertEqual(valid, True)

    def test_find_block_salt(self):
        open_transaction = [{"sender": "Marc", "recipient": "Bob", "amount": 100}]
        previous_hash = (
            "076f74c1e78bceb14a65775013948f24eaacc3ac1bc7e3e911fe4aa3ae198c7"
        )
        salt = blockchain.find_block_salt(open_transaction, previous_hash)
        self.assertEqual(19, salt)

    @patch("blockchain.get_last_blockchain_value")
    def test_invalid_proof(self, get_last_blockchain_value):
        blockchain.open_transaction = self.get_open_transaction_stub()
        valid = blockchain.valid_salt(blockchain.open_transaction, "previous_hash", 20)
        get_last_blockchain_value.called
        self.assertEqual(valid, False)

    def get_open_transaction_stub(self):
        return [{"sender": "Marc", "recipient": "Bob", "amount": 100}]

    def get_blockchain_stub(self):
        return [
            genesis_block,
            {
                "previous_hash": "00",
                "index": 1,
                "transactions": [
                    {"sender": "Marc", "recipient": "Bob", "amount": 100},
                    {"sender": "Marc", "recipient": "Bob", "amount": 100},
                ],
            },
        ]

    @patch(
        "blockchain.get_last_blockchain_value",
        return_value={
            "transactions": [
                {"sender": "Marc", "recipient": "Bob", "amount": 100},
                {"sender": "Marc", "recipient": "Bob", "amount": 100},
            ],
        },
    )
    def test_get_user_balance(self, get_last_blockchain_value):
        bobBalance = blockchain.get_user_balance("Bob")
        marcBalance = blockchain.get_user_balance("Marc")
        self.assertEqual(bobBalance, 200)
        self.assertEqual(marcBalance, -200)
        get_last_blockchain_value.called

    def test_it_can_add_a_transaction_to_the_open_transaction_queue(self):
        blockchain.add_transaction(
            recipient="Bob",
            sender="Marc",
            amount=10,
        )
        self.assertEqual(
            blockchain.open_transaction,
            [{"amount": 10, "recipient": "Bob", "sender": "Marc"}],
        )

    def test_it_can_add_a_participant(self):
        global blockchain
        blockchain.participants.add("Paul")
        self.assertEqual(blockchain.participants, set({"Paul", "Marc"}))

    def int_test_blockchain_is_valid(self):
        stub_blockchain = []
        open_transaction = []
        blockchain.add_transaction(recipient="Bob", sender="Marc", amount=10)
        blockchain.mine_block(stub_blockchain, open_transaction)
        blockchain.add_transaction(recipient="Tom", sender="Marc", amount=10)
        blockchain.mine_block(stub_blockchain, open_transaction)
        is_valid = blockchain.verify_chain(blockchain)
        self.assertTrue(is_valid)

    @patch("blockchain.get_user_input", side_effect=["1", "Bob", "10", "q"])
    def test_add_transaction_api(self, get_user_input):
        blockchain.grouped_transaction()
        assert get_user_input.called

    @patch("blockchain.get_last_blockchain_value")
    def test_hash_a_blockchain(self, get_last_blockchain_value):
        previous_hash = (
            "076f74c1e78bceb14a65775013948f24eaacc3ac1bc7e3e911fe4aa3ae198c7"
        )
        salt = 0
        hash = ""
        while hash[0:1] != "0":
            salt = salt + 1
            hash = blockchain.hash_block([], previous_hash, salt)
        get_last_blockchain_value.called
        self.assertEqual(hash[0:1], "0")

    def test_it_can_list_participants(self):
        participants = set({"Marc"})
        self.assertEqual(blockchain.output_participant(participants), participants)

    def test_it_can_output_user_balance(self):
        blockchain.blockchain = self.get_blockchain_stub()
        self.assertEqual(blockchain.get_user_balance("Marc"), -200)

    def test_user_wants_to_add_a_new_transaction(self):
        self.assertTrue(blockchain.user_wants_to_add_a_new_transaction(1))

    def test_user_wants_to_output_the_blockchain(self):
        self.assertTrue(blockchain.user_wants_to_output_the_blockchain(2))

    def test_user_wants_to_mind_new_block(self):
        self.assertTrue(blockchain.user_wants_to_mind_new_block(3))

    def test_user_wants_to_output_participants(self):
        self.assertTrue(blockchain.user_wants_to_output_participants(4))

    def test_user_wants_to_output_the_blockchain_falsy(self):
        self.assertFalse(blockchain.user_wants_to_add_a_new_transaction(None))

    def test_user_wants_to_add_a_new_transaction_falsy(self):
        self.assertFalse(blockchain.user_wants_to_add_a_new_transaction(None))


if __name__ == "__main__":
    unittest.main()
