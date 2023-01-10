import unittest
from block import Block
from tests.mock_utils import genesis_block
from utils.helpers import isfloat

class TestBlock(unittest.TestCase):
    def test_create_block_instance(self):
        instance = Block(genesis_block)
        block = instance.__dict__
        assert block["index"] == genesis_block["index"]
        assert block["previous_hash"] == genesis_block["previous_hash"]
        assert block["transactions"] == genesis_block["transactions"]
        assert block["salt"] == genesis_block["salt"]
        assert isfloat(block["created_at"])
