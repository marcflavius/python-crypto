""" Blockchain lib """

from functools import reduce
import json
import os.path
from block import Block, PrimeBlock
from typing import Type
from transaction import Transaction, PrimeTransaction
from log import Log
from member import Member
from utils.printable import Printable
from utils.primeable import Primeable
from verification import Verification

# TODO: Add OrderedDict logic to prevent block validation failure due to dict reordering
# TODO: Add pickle to store binary data (can be swapped by json)
# TODO: Add OOP
# members - done,
# transaction - done,
# block - done,
# verification - done,
# node
# TODO: Add OOP create a printable helper class to output class __repr__

genesis_block: PrimeBlock = {
    "previous_hash": "GENESIS_BLOCK",
    "index": 0,
    "transactions": [],
    "salt": 0,
}
blockchain = []
open_transaction: list[Transaction] = []
MINING_TRANSACTION: int = 5


class Blockchain(Printable):
    def __init__(
        self,
        owner: str,
        init_chain: list[Block] = [],
        init_transactions: list[Transaction] = [],
        blockchain_location_path: str | None = None,
    ):
        self.owner = owner
        self.blockchain: list[Block] = init_chain[:]
        self.open_transaction: list[Transaction] = init_transactions[:]
        self.participants = Member()
        self.participants.add(owner)
        self.blockchain_location_path = (
            "blockchain.txt"
            if blockchain_location_path is None
            else blockchain_location_path
        )

    def get_prime(self, subject):
        output = []
        if subject.__name__ == Transaction.__name__ and len(self.open_transaction) > 0:
            mapping = self.open_transaction
        elif subject.__name__ == Block.__name__:
            mapping = self.open_transaction
        else:
            return []
        for item in mapping:
            print("item:", item)

            output.append(item.to_prime())
        return output

    def reset_blockchain(self):
        """Wipe the blockchain"""
        self.blockchain = []

    def get_last_blockchain_value(self):
        """Get the last element in the blockchain"""
        global genesis_block
        return self.blockchain[-1] if len(self.blockchain) > 0 else Block(genesis_block)

    def mine_block(self):
        """add all open transaction to a block and wipe
        the open transaction array"""
        previous_hash = self.get_last_blockchain_value().previous_hash
        old_blockchain = self.blockchain[:]
        reward_transaction: PrimeTransaction = {
            "sender": "MINING",
            "recipient": self.owner,
            "amount": MINING_TRANSACTION,
        }
        self.open_transaction.append(Transaction(reward_transaction))
        # hashing
        salt = Verification.find_block_salt(self.get_prime(Transaction), previous_hash)
        current_hash = Verification.hash_block(
            self.get_prime(Transaction), previous_hash, salt
        )
        new_block = Block(
            {
                "previous_hash": current_hash,
                "index": len(self.blockchain),
                "transactions": self.open_transaction[:],
                "salt": salt,
            }
        )
        self.blockchain.append(new_block)

        valid, index = Verification.verify_chain(self.blockchain)
        if valid:
            self.save_blockchain()
            self.open_transaction.clear()
            Log.log("Block added!")
        else:
            # revert
            self.revert_chain(old_blockchain)
            Log.log("Invalid chain! at index {}".format(index))

    def revert_chain(self, old_blockchain):
        self.blockchain.clear()
        for block in old_blockchain:
            self.blockchain.append(block)

    def output_blockchain(self, given_blockchain):
        """Output the block chain"""
        for block in given_blockchain:
            print("Outputting block...")
            print(block)

    def output_participant(self):
        print(self.participants)

    def output_open_transactions(self, open_transactions):
        print(open_transactions)
        return open_transaction

    def get_user_balance(self, user_id):
        last_block = self.get_last_blockchain_value()
        transactions = last_block.transactions

        def balance(total, transaction):
            amount = transaction["amount"]
            if transaction["recipient"] == user_id:
                return total + amount
            if transaction["sender"] == user_id:
                return total - amount
            else:
                return total

        total = reduce(balance, transactions, 0)
        return total

    def output_user_balance(self, user_id):
        balance = self.get_user_balance(user_id)
        print(balance)
        return balance

    def load_blockchain(self, blockchain_location_path):
        file_exists = os.path.exists(blockchain_location_path)
        if not file_exists:
            self.create_blockchain_file_store(blockchain_location_path)
        self.hydrate_blockchain(blockchain_location_path)
        if len(self.blockchain) == 0:
            Log.log("Init blockchain")
            blockchain.append(genesis_block)

    def hydrate_blockchain(self, blockchain_location_path="blockchain.txt"):

        try:
            with open(self.blockchain_location_path, encoding="utf-8", mode="r") as f:
                data = json.load(f)
                self.blockchain = data["blockchain"]
                self.open_transaction = data["open_transaction"]
        except IOError:
            Log.log(
                "Can't read the blockchain filestore {}".format(
                    blockchain_location_path
                )
            )
        except ValueError:
            Log.log(
                "{} parse failed, file format incorrect.".format(
                    blockchain_location_path
                )
            )

    def create_blockchain_file_store(self, blockchain_location_path):
        try:
            with open(blockchain_location_path, encoding="utf-8", mode="w"):
                self.save_blockchain()
        except IOError:
            Log.log("Can't create the file {}".format(blockchain_location_path))

    def save_blockchain(self):

        try:
            with open(self.blockchain_location_path, encoding="utf-8", mode="w") as f:
                data = json.dumps(
                    {
                        "blockchain": self.get_prime(Block),
                        "open_transaction": self.get_prime(Transaction),
                    },
                    indent=4,
                )
                f.write(data)
        except IOError:
            Log.log("can't write to file {}.".format(self.blockchain_location_path))
