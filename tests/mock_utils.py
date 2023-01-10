from block import Block, PrimeBlock
from transaction import PrimeTransaction

genesis_block: PrimeBlock = {
    "previous_hash": "GENESIS_BLOCK",
    "index": 0,
    "transactions": [],
    "salt": 22,
}
derived_from_genesis_block: PrimeBlock = {
    "previous_hash": "0cdfe6d341443fb03e149add1696d83da65e8ca9ed7a19e28cda0212c45dbf89",
    "index": 1,
    "transactions": [],
    "salt": 11,
}
falsy_derivation_of_genesis_block: PrimeBlock = {
    "previous_hash": "0cdfe6d341443fb03e149add1696d83da65e8ca9ed7a19e28cda0212c45dbf89",
    "index": 1,
    "transactions": [],
    "salt": 22,
}


def generate_single_transaction(
    sender="Marc", recipient="Bob", amount=10
) -> PrimeTransaction:
    return {"sender": sender, "recipient": recipient, "amount": amount}


def get_open_transaction_stub():
    return [{"sender": "Marc", "recipient": "Bob", "amount": 100}]

def get_blockchain_stub():
    return [
        Block(genesis_block),
        Block(
            {
                "salt": 0,
                "previous_hash": "00",
                "index": 1,
                "transactions": [
                    {"sender": "Marc", "recipient": "Bob", "amount": 100},
                    {"sender": "Marc", "recipient": "Bob", "amount": 100},
                ],
            }
        ),
    ]
