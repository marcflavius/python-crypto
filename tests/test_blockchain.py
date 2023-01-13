import json
import unittest
from unittest.mock import MagicMock, patch, mock_open
from block import Block
from node import Node
from log import Log
from transaction import Transaction
from verification import Verification
from blockchain import Blockchain
from tests.mock_utils import (
    derived_from_genesis_block,
    falsy_derivation_of_genesis_block,
    generate_single_transaction,
    genesis_block,
    get_blockchain_stub,
    none_derived_block_with_transaction,
)
from utils.helpers import isfloat


class TestBlockchain(unittest.TestCase):
    def setUp(self):
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    # (start)

    def test_map_to_prime(self):
        open_transaction: list[Transaction] = [
            Transaction(generate_single_transaction())
        ]
        given_blockchain: list[Block] = [Block(none_derived_block_with_transaction)]
        blockchain = Blockchain("Marc", given_blockchain, open_transaction)
        block_prime_list = blockchain.map_to_prime(Block)
        block_prime_list[0].pop("created_at")
        block_prime_list[0]["transactions"][0].pop("created_at")
        # block_prime_list.("created_at")
        assert block_prime_list == [
            {
                "previous_hash": "GENESIS_BLOCK",
                "index": 0,
                "transactions": [{"sender": "Marc", "recipient": "Bob", "amount": 100}],
                "salt": 22,
            }
        ]

    def test_hydrate_blockchain_success(self):
        blockchain = Blockchain("Marc")
        open_transaction = [generate_single_transaction()]
        given_chain = [genesis_block, derived_from_genesis_block]
        data = json.dumps(
            {
                "blockchain": given_chain,
                "open_transaction": open_transaction,
            },
            indent=4,
        )
        with patch("builtins.open", mock_open(read_data=data)):
            blockchain.hydrate_blockchain("blockchain.txt")
            open.assert_called_with("blockchain.txt", encoding="utf-8", mode="r")
            assert all(isinstance(n, Block) for n in blockchain.blockchain) is True
            assert all(isinstance(n, Transaction) for n in blockchain.open_transaction) is True

    @patch.object(Log, "log")
    def test_hydrate_blockchain_fails_on_io_error(self, logger):
        blockchain = Blockchain("Marc")
        mockOpen = mock_open()
        mockOpen.side_effect = IOError
        with patch("builtins.open", mockOpen):
            blockchain.hydrate_blockchain("blockchain.txt")
            assert logger.called
            logger.assert_called_with(
                "Can't read the blockchain filestore blockchain.txt"
            )

    @patch.object(Log, "log")
    def test_hydrate_blockchain_on_json_parse_error(self, logger):
        blockchain = Blockchain("Marc")
        mockOpen = mock_open()
        mockOpen.side_effect = ValueError 
        with patch("builtins.open", mockOpen):
            blockchain.hydrate_blockchain("blockchain.txt")
            assert logger.called
            logger.assert_called_with(
            "blockchain.txt parse failed, file format incorrect."
            )
        mockOpen.side_effect = AttributeError 
        with patch("builtins.open", mockOpen):
            blockchain.hydrate_blockchain("blockchain.txt")
            assert logger.called
            logger.assert_called_with(
            "blockchain.txt parse failed, file format incorrect."
            )

    def test_save_blockchain_success(self):
        blockchain = Blockchain(
            "Marc", [Block(genesis_block)], [Transaction(generate_single_transaction())]
        )
        data = json.dumps(
            {
                "blockchain": blockchain.map_to_prime(Block),
                "open_transaction": blockchain.map_to_prime(Transaction),
            },
            indent=4,
        )
        with patch("builtins.open", mock_open()) as file_handle:
            blockchain.save_blockchain()
            open.assert_called_with("blockchain.txt", encoding="utf-8", mode="w")
            file_handle.return_value.write.assert_called_with(data)

    @patch.object(Log, "log")
    def test_save_blockchain_fails_on_file_access(self, logger):
        blockchain = Blockchain("Marc")
        mockOpen = mock_open()
        mockOpen.side_effect = IOError
        with patch("builtins.open", mockOpen):
            blockchain.save_blockchain()
        logger.assert_called_with("can't write to file blockchain.txt.")

    @patch("os.path.exists", return_value=False)
    @patch.object(Blockchain, "create_blockchain_file_store")
    @patch.object(Blockchain, "hydrate_blockchain")
    @patch.object(Log, "log")
    def test_load_blockchain_success_on_create_filestore(
        self,
        logger,
        hydrate_blockchain,
        create_blockchain_file_store,
        exists,
    ):
        blockchain = Blockchain("Marc")
        blockchain.load_blockchain("test_blockchain.txt")
        assert exists.called
        assert create_blockchain_file_store.called
        assert hydrate_blockchain.called
        logger.assert_called_with("Init blockchain")

    @patch.object(Log, "log")
    @patch.object(Blockchain, "hydrate_blockchain")
    @patch.object(Blockchain, "create_blockchain_file_store")
    @patch("os.path.exists", return_value=True)
    def test_load_blockchain_success_on_init_filestore(
        self,
        exists,
        create_blockchain_file_store,
        hydrate_blockchain,
        logger,
    ):
        blockchain = Blockchain("Marc")
        blockchain.load_blockchain("test_blockchain.txt")
        assert exists.called
        assert not create_blockchain_file_store.called
        assert hydrate_blockchain.called
        assert logger.called
        # assert logger.log.called_with("Init blockchain")

    @patch.object(Log, "log")
    @patch.object(Blockchain, "hydrate_blockchain")
    @patch.object(Blockchain, "create_blockchain_file_store")
    @patch("os.path.exists", return_value=True)
    def test_load_blockchain_success_on_filestore_reload(
        self,
        exists,
        create_blockchain_file_store,
        hydrate_blockchain,
        logger,
    ):
        blockchain = Blockchain("Marc")
        blockchain.blockchain = [Block(genesis_block)]
        blockchain.load_blockchain("test_blockchain.txt")
        assert exists.called
        assert not create_blockchain_file_store.called
        assert hydrate_blockchain.called
        assert not logger.called

    @patch.object(
        Blockchain,
        "get_last_blockchain_value",
        side_effect=[Block(derived_from_genesis_block)],
    )
    @patch.object(
        Verification,
        "hash_block",
        side_effect=[
            "0412a7b5869a471587e0fa102ad717055fbcde7e2fd2c22c03f0590f71f71b96"
        ],
    )
    @patch.object(Verification, "verify_chain", side_effect=[(True, 0), (True, 1)])
    @patch.object(Log, "log")
    def test_mind_block_success(
        self,
        logger,
        verify_chain,
        hash_block,
        get_last_blockchain_value,
    ):
        with patch("builtins.open", mock_open()):
            init_blockchain = [Block(genesis_block), Block(derived_from_genesis_block)]
            blockchain = Blockchain("Marc", init_blockchain[:])
            blockchain.open_transaction.append(
                Transaction(
                    {
                        "sender": "Marc",
                        "recipient": "Bob",
                        "amount": 100,
                    }
                )
            )
            blockchain.save_blockchain = MagicMock(return_value=None)
            blockchain.mine_block()
            self.assertEqual(len(blockchain.blockchain), 3)
            self.assertEqual(blockchain.blockchain[0].index, 0)
            self.assertEqual(blockchain.blockchain[1].index, 1)
            self.assertEqual(blockchain.blockchain[2].index, 2)
            get_last_blockchain_value.called
            hash_block.called
            verify_chain.called
            logger.called
            logger.assert_called_with("Block added!")
            self.assertEqual(len(init_blockchain), 2)
            self.assertEqual(len(blockchain.blockchain), 3)
            self.assertEqual(len(blockchain.blockchain[2].transactions), 2)
            self.assertEqual(len(blockchain.open_transaction), 0)

    @patch.object(
        Blockchain,
        "get_last_blockchain_value",
        side_effect=[Block(derived_from_genesis_block)],
    )
    @patch.object(
        Verification,
        "hash_block",
        side_effect=[
            "0412a7b5869a471587e0fa102ad717055fbcde7e2fd2c22c03f0590f71f71b96"
        ],
    )
    @patch.object(Verification, "verify_chain", side_effect=[(False, 0)])
    @patch.object(Log, "log")
    def test_mind_block_fails(
        self, get_last_blockchain_value, hash_block, verify_chain, logger
    ):
        given_blockchain = [
            Block(genesis_block),
            Block(falsy_derivation_of_genesis_block),
        ]
        blockchain = Blockchain("Marc", given_blockchain)
        init_blockchain = given_blockchain[:]
        blockchain.mine_block()
        self.assertEqual(given_blockchain[0].index, 0)
        self.assertEqual(given_blockchain[1].index, 1)
        get_last_blockchain_value.called
        hash_block.called
        verify_chain.called
        logger.called
        logger.log.called_with("Invalid chain!")
        self.assertEqual(len(init_blockchain), 2)
        self.assertEqual(len(given_blockchain), 2)

    def test_get_last_blockchain_value(self):
        init_blockchain = [Block(genesis_block), Block(derived_from_genesis_block)]
        blockchain = Blockchain("Marc", init_blockchain)
        last_block = blockchain.get_last_blockchain_value()
        self.assertIsInstance(last_block, Block)

    @patch.object(
        Blockchain,
        "get_last_blockchain_value",
        return_value=Block(
            {
                "index": 0,
                "previous_hash": "stub",
                "salt": 0,
                "transactions": [
                    {"sender": "Marc", "recipient": "Bob", "amount": 100},
                    {"sender": "Marc", "recipient": "Bob", "amount": 100},
                ],
            }
        ),
    )
    def test_get_user_balance(self, get_last_blockchain_value):
        blockchain = Blockchain("Marc")
        bobBalance = blockchain.get_user_balance("Bob")
        marcBalance = blockchain.get_user_balance("Marc")
        self.assertEqual(bobBalance, 200)
        self.assertEqual(marcBalance, -200)
        get_last_blockchain_value.called

    def test_it_can_add_a_transaction_to_the_open_transaction_queue(self):
        open_transaction = [{"amount": 10, "recipient": "Bob", "sender": "Marc"}]
        blockchain = Blockchain("Marc")
        node = Node(blockchain, blockchain.owner)
        node.add_transaction(
            recipient="Bob",
            sender="Marc",
            amount=10,
        )
        self.assertEqual(len(blockchain.open_transaction), len(open_transaction))

    def test_it_can_add_a_participant(self):
        blockchain = Blockchain("Marc")
        blockchain.participants.add("Paul")
        self.assertEqual(blockchain.participants.all(), set({"Paul", "Marc"}))

    def int_test_blockchain_is_valid(self):
        blockchain = Blockchain("Marc")
        node = Node(blockchain, blockchain.owner)
        node.add_transaction(recipient="Bob", sender="Marc", amount=10)
        blockchain.mine_block()
        node.add_transaction(recipient="Tom", sender="Marc", amount=10)
        blockchain.mine_block()
        is_valid = Verification.verify_chain(blockchain)
        self.assertTrue(is_valid)

    @patch.object(Blockchain, "get_last_blockchain_value")
    def test_hash_a_blockchain(self, get_last_blockchain_value):
        previous_hash = (
            "076f74c1e78bceb14a65775013948f24eaacc3ac1bc7e3e911fe4aa3ae198c7"
        )
        salt = 0
        hash = ""
        while hash[0:1] != "0":
            salt = salt + 1
            hash = Verification.hash_block([], previous_hash, salt)
        get_last_blockchain_value.called
        self.assertEqual(hash[0:1], "0")

    @patch.object(Node, "get_user_input", side_effect=["1"])
    def test_get_user_choice(self, get_user_input):
        user_choice = Node.get_user_choice(
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

    @patch("builtins.print")
    def test_it_can_list_participants(self, print_mock):
        blockchain = Blockchain("Marc")
        blockchain.output_participant()
        print_mock.assert_called_with(blockchain.participants)

    def test_it_can_output_user_balance(self):
        blockchain = Blockchain("Marc")
        blockchain.blockchain = get_blockchain_stub()
        self.assertEqual(blockchain.get_user_balance("Marc"), -200)


if __name__ == "__main__":
    unittest.main()
