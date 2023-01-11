import unittest
from unittest.mock import patch
import blockchain
from transaction import Transaction
from verification import Verification
from blockchain import Blockchain
from tests.mock_utils import (
    generate_single_transaction,
    get_prime_blockchain_stub,
    get_prime_open_transaction_stub,
    derived_from_genesis_block,
    genesis_block,
)


class TestVerification(unittest.TestCase):
    @patch.object(Verification, "find_block_salt", return_value=22)
    def test_verify_the_chain_with_one_block(self, find_block_salt):
        blockchain.blockchain = [genesis_block]
        valid = Verification.verify_chain(blockchain.blockchain)
        self.assertEqual(valid, (True, 0))
        find_block_salt.called

    def test_verify_the_chain_with_multi_block_fail(self):
        blockchain.blockchain = [genesis_block, genesis_block]
        valid = Verification.verify_chain(blockchain.blockchain)
        self.assertEqual(valid, (False, 1))

    @patch.object(Verification, "_blockchain_has_zero_or_one_block", return_value=False)
    @patch.object(Verification, "_is_first_block", side_effect=[True, False])
    @patch.object(
        Verification,
        "hash_block",
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
        valid = Verification.verify_chain(stub_blockchain)
        self.assertEqual(valid, (True, 1))
        assert _blockchain_has_zero_or_one_block.called
        Verification._blockchain_has_zero_or_one_block.assert_called_with(
            init_stub_blockchain
        )
        assert _is_first_block.called
        assert hash_block.called
        Verification._is_first_block.assert_called_with(1)

    @patch.object(
        Blockchain,
        "get_last_blockchain_value",
        return_value={
            "transactions": [],
            "previous_hash": "00",
            "index": 1,
            "previous_hash": "076f74c1e78bceb14a65775013948f24eaacc3ac1bc7e3e911fe4aa3ae198c7",
        },
    )
    def test_valid_salt(self, get_last_blockchain_value):
        blockchain = Blockchain("Marc")
        blockchain.open_transaction = [Transaction(generate_single_transaction())]
        previous_hash = blockchain.get_last_blockchain_value()["previous_hash"]  # type: ignore for mock purpose
        salt = Verification.find_block_salt(
            blockchain.map_to_prime(Transaction), previous_hash
        )
        valid = Verification.valid_salt(
            blockchain.map_to_prime(Transaction), previous_hash, salt
        )
        get_last_blockchain_value.called
        self.assertEqual(valid, True)

    @patch.object(Blockchain, "get_last_blockchain_value")
    def test_invalid_proof(self, get_last_blockchain_value):
        valid = Verification.valid_salt(
            get_prime_blockchain_stub(), "previous_hash", 20
        )
        get_last_blockchain_value.called
        self.assertEqual(valid, False)

    def test_find_block_salt(self):
        open_transaction = get_prime_open_transaction_stub()
        previous_hash = (
            "076f74c1e78bceb14a65775013948f24eaacc3ac1bc7e3e911fe4aa3ae198c7"
        )
        salt = Verification.find_block_salt(open_transaction, previous_hash)
        self.assertEqual(19, salt)
