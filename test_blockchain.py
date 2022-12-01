import json
import unittest
from unittest.mock import patch, mock_open
from block import Block
import blockchain
from transaction import Transaction

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

    def isfloat(self, num):
        try:
            float(num)
            return True
        except ValueError:
            return False

    # (start)
    
    
    def test_create_transaction_instance(self):
        givenTransaction = self.generate_transaction()
        instance = Transaction(givenTransaction)
        transactionOfInstance = instance.__dict__
        assert transactionOfInstance["sender"] == givenTransaction["sender"]
        assert transactionOfInstance["recipient"] == givenTransaction["recipient"]
        assert transactionOfInstance["amount"] == givenTransaction["amount"]
        assert self.isfloat(transactionOfInstance['created_at']) 

    def test_create_block_instance(self):
        instance = Block(genesis_block)
        block = instance.__dict__
        assert block["index"] == genesis_block["index"]
        assert block["previous_hash"] == genesis_block["previous_hash"]
        assert block["transactions"] == genesis_block["transactions"]
        assert block["salt"] == genesis_block["salt"]
        assert self.isfloat(block['created_at']) 

    def test_hydrate_blockchain_success(self):
        open_transaction = [self.generate_transaction()]
        given_blockchain = [genesis_block, derived_from_genesis_block]
        data = json.dumps(
            {
                "blockchain": given_blockchain,
                "open_transaction": open_transaction,
            },
            indent=4,
        )
        with patch("builtins.open", mock_open(read_data=data)):
            restored_blockchain, open_transaction = blockchain.hydrate_blockchain(
                "blockchain.txt"
            )
            open.assert_called_with("blockchain.txt", encoding="utf-8", mode="r")
            self.assertEqual(restored_blockchain, given_blockchain)
            self.assertEqual(open_transaction, open_transaction)

    @patch("blockchain.logger")
    def test_hydrate_blockchain_fails_on_io_error(self, logger):
        mockOpen = mock_open()
        mockOpen.side_effect = IOError
        with patch("builtins.open", mockOpen):
            blockchain.hydrate_blockchain("blockchain.txt")
            logger.assert_called_with(
                "Can't read the blockchain filestore blockchain.txt"
            )

    @patch("blockchain.logger")
    def test_hydrate_blockchain_on_json_parse_error(self, logger):
        mockOpen = mock_open()
        mockOpen.side_effect = ValueError
        with patch("builtins.open", mockOpen):
            blockchain.hydrate_blockchain("blockchain.txt")
            logger.assert_called_with(
                "blockchain.txt parse failed, file format incorrect."
            )

    def test_save_blockchian_success(self):
        data = json.dumps(
            {
                "blockchain": blockchain.blockchain,
                "open_transaction": blockchain.open_transaction,
            },
            indent=4,
        )
        with patch("builtins.open", mock_open()) as file_handle:
            blockchain.save_blockchain(
                blockchain.blockchain, blockchain.open_transaction
            )
            open.assert_called_with("blockchain.txt", encoding="utf-8", mode="w")
            file_handle.return_value.write.assert_called_with(data)

    @patch("blockchain.logger")
    def test_save_blockchian_fails_on_file_access(self, logger):
        mockOpen = mock_open()
        mockOpen.side_effect = IOError
        with patch("builtins.open", mockOpen):
            blockchain.save_blockchain(
                blockchain.blockchain, blockchain.open_transaction
            )
        logger.assert_called_with("can't write to file blockchain.txt.")

    @patch("blockchain.logger")
    @patch("blockchain.hydrate_blockchain")
    @patch("blockchain.create_blockchain_file_store")
    @patch("os.path.exists", return_value=False)
    def test_load_blockchain_success_on_create_filestore(
        self,
        exists,
        create_blockchain_file_store,
        hydrate_blockchain,
        logger,
    ):
        blockchain.blockchain = []
        blockchain.load_blockchain("test_blockchain.txt")
        assert exists.called
        assert create_blockchain_file_store.called
        assert hydrate_blockchain.called
        assert logger.called
        assert blockchain.logger.called_with("Init blockchain")

    @patch("blockchain.logger")
    @patch("blockchain.hydrate_blockchain")
    @patch("blockchain.create_blockchain_file_store")
    @patch("os.path.exists", return_value=True)
    def test_load_blockchain_success_on_init_filestore(
        self,
        exists,
        create_blockchain_file_store,
        hydrate_blockchain,
        logger,
    ):
        blockchain.blockchain = []
        blockchain.load_blockchain("test_blockchain.txt")
        assert exists.called
        assert not create_blockchain_file_store.called
        assert hydrate_blockchain.called
        assert logger.called
        assert blockchain.logger.called_with("Init blockchain")

    @patch("blockchain.logger")
    @patch("blockchain.hydrate_blockchain")
    @patch("blockchain.create_blockchain_file_store")
    @patch("os.path.exists", return_value=True)
    def test_load_blockcain_success_on_filestore_reload(
        self,
        exists,
        create_blockchain_file_store,
        hydrate_blockchain,
        logger,
    ):
        blockchain.blockchain = [genesis_block]
        blockchain.load_blockchain("test_blockchain.txt")
        assert exists.called
        assert not create_blockchain_file_store.called
        assert hydrate_blockchain.called
        assert not logger.called

    @patch("blockchain.load_blockchain")
    @patch("blockchain.controller")
    @patch("blockchain.logger")
    def test_main(self, load_blockchain, controller, looger):
        blockchain.main()
        blockchain.blockchain = []
        blockchain.open_transaction = [self.generate_transaction()]
        assert load_blockchain.called
        assert controller.called
        assert looger.called
        blockchain.logger.called_with("Good Bye!")
        self.assertEqual(blockchain.blockchain, [])

    @patch(
        "blockchain.get_last_blockchain_value", side_effect=[derived_from_genesis_block]
    )
    @patch(
        "blockchain.hash_block",
        side_effect=[
            "0412a7b5869a471587e0fa102ad717055fbcde7e2fd2c22c03f0590f71f71b96"
        ],
    )
    @patch("blockchain.verify_chain", side_effect=[(True, 0), (True, 1)])
    @patch("blockchain.logger")
    def test_mind_block_success(
        self, get_last_blockchain_value, hash_block, verify_chain, logger
    ):
        init_blockchain = [genesis_block, derived_from_genesis_block]
        blockchain.blockchain = init_blockchain[:]
        blockchain.open_transaction.append(
            {"sender": "Marc", "recipient": "Bob", "amount": 100}
        )
        blockchain.mine_block(blockchain.blockchain, blockchain.open_transaction)
        self.assertEqual(len(blockchain.blockchain), 3)
        self.assertEqual(blockchain.blockchain[0]["index"], 0)
        self.assertEqual(blockchain.blockchain[1]["index"], 1)
        self.assertEqual(blockchain.blockchain[2]["index"], 2)
        get_last_blockchain_value.called
        hash_block.called
        verify_chain.called
        logger.called
        blockchain.logger.assert_called_with("Block added!")
        self.assertEqual(len(init_blockchain), 2)
        self.assertEqual(len(blockchain.blockchain), 3)
        self.assertEqual(len(blockchain.blockchain[2]["transactions"]), 2)
        self.assertEqual(len(blockchain.open_transaction), 0)

    @patch(
        "blockchain.get_last_blockchain_value", side_effect=[derived_from_genesis_block]
    )
    @patch(
        "blockchain.hash_block",
        side_effect=[
            "0412a7b5869a471587e0fa102ad717055fbcde7e2fd2c22c03f0590f71f71b96"
        ],
    )
    @patch("blockchain.verify_chain", side_effect=[(False, 0)])
    @patch("blockchain.logger")
    def test_mind_block_fails(
        self, get_last_blockchain_value, hash_block, verify_chain, logger
    ):
        given_blockchain = [genesis_block, falsy_derivation_of_genesis_block]
        init_blockchain = given_blockchain[:]
        open_transaction = []
        blockchain.mine_block(given_blockchain, open_transaction)
        self.assertEqual(given_blockchain[0]["index"], 0)
        self.assertEqual(given_blockchain[1]["index"], 1)
        get_last_blockchain_value.called
        hash_block.called
        verify_chain.called
        logger.called
        blockchain.logger.called_with("Invalid chain!")
        self.assertEqual(len(init_blockchain), 2)
        self.assertEqual(len(given_blockchain), 2)

    @patch("blockchain.find_block_salt", return_value=22)
    def test_verify_the_chain_with_one_block(self, find_block_salt):
        blockchain.blockchain = [genesis_block]
        valid = blockchain.verify_chain(blockchain.blockchain)
        self.assertEqual(valid, (True, 0))
        find_block_salt.called

    def test_verify_the_chain_with_multi_block_fail(self):
        blockchain.blockchain = [genesis_block, genesis_block]
        valid = blockchain.verify_chain(blockchain.blockchain)
        self.assertEqual(valid, (False, 1))

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
        self.assertEqual(valid, (True, 1))
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
        open_transaction = [self.generate_transaction()]
        previous_hash = blockchain.get_last_blockchain_value()["previous_hash"]
        salt = blockchain.find_block_salt(open_transaction, previous_hash)
        valid = blockchain.valid_salt(open_transaction, previous_hash, 19)
        get_last_blockchain_value.called
        self.assertEqual(valid, True)

    def generate_transaction(self):
        return {"sender": "Marc", "recipient": "Bob", "amount": 100}

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

    @patch("blockchain.get_user_choice", side_effect=[("1", [1]), ("q", ["q"])])
    @patch("blockchain.get_user_transaction", side_effect=[(10, "Bob")])
    def test_controller_add_transaction_success(
        self,
        get_user_choice,
        get_user_transaction,
    ):
        blockchain.controller()
        assert get_user_choice.called
        assert get_user_transaction.called
        assert blockchain.open_transaction == [
            {"sender": "Marc", "recipient": "Bob", "amount": 10}
        ]

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

    @patch("blockchain.get_user_input", side_effect=["1"])
    def test_get_user_choice(self, get_user_input):
        user_choice = blockchain.get_user_choice(
            """
            Please choose
            1: Add a new transaction value
            5: List open transactions
            6: Output user balance
            q: To Quit
        """
        )
        assert get_user_input.called
        self.assertEqual(user_choice, ("1", ["1", "5", "6", "q"]))

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
