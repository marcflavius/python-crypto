""" Blockchain lib """

from functools import reduce
import json
import os.path
from log import Log
from member import Member
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

genesis_block = {
    "previous_hash": "GENESIS_BLOCK",
    "index": 0,
    "transactions": [],
}
blockchain = []
open_transaction = []
MINING_TRANSACTION = 5


class Blockchain:
    def __init__(self, owner, init_chain: list=[], init_transactions:list=[], blockchain_location_path:str | None=None):

        self.owner = owner
        self.blockchain = init_chain[]
        self.open_transaction = init_transactions[:]
        self.participants = Member()
        self.participants.add(owner)
        self.blockchain_location_path = (
            "blockchain.txt"
            if blockchain_location_path is None
            else blockchain_location_path
        )

    def reset_blockchain(self):
        """Wipe the blockchain"""
        self.blockchain = []

    def get_last_blockchain_value(self, givin_blockchain=None):
        """Get the last element in the blockchain"""
        global genesis_block
        used_blockchain = (
            self.blockchain if givin_blockchain == None else givin_blockchain
        )
        return used_blockchain[-1] if len(used_blockchain) > 0 else genesis_block

    def mine_block(self):
        """Add all open transaction to a block and wipe
        the open transaction array"""
        previous_hash = self.get_last_blockchain_value(self.blockchain)["previous_hash"]
        old_blockchain = self.blockchain[:]
        reward_transaction = {
            "sender": "MINING",
            "recipient": self.owner,
            "amount": MINING_TRANSACTION,
        }
        self.open_transaction.append(reward_transaction)
        # hashing
        salt = Verification.find_block_salt(self.open_transaction, previous_hash)
        current_hash = Verification.hash_block(
            self.open_transaction, previous_hash, salt
        )
        new_block = {
            "previous_hash": current_hash,
            "index": len(self.blockchain),
            "transactions": self.open_transaction[:],
            "salt": salt,
        }
        self.blockchain.append(new_block)

        valid, index = Verification.verify_chain(self.blockchain)
        if valid:
            self.save_blockchain(self.blockchain, [])
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
        transactions = last_block["transactions"]

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
                self.save_blockchain(self.blockchain, self.open_transaction)
        except IOError:
            Log.log("Can't create the file {}".format(blockchain_location_path))

    def save_blockchain(self, blockchain, open_transaction):
        try:
            with open(self.blockchain_location_path, encoding="utf-8", mode="w") as f:
                data = json.dumps(
                    {
                        "blockchain": blockchain,
                        "open_transaction": open_transaction,
                    },
                    indent=4,
                )
                f.write(data)
        except IOError:
            Log.log("can't write to file {}.".format(self.blockchain_location_path))
