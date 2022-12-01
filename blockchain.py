""" Blockchain lib """
import hashlib as hash
import re
import json
from functools import reduce
import os.path

# TODO: Add OrderedDict logic to prevent block validation failure due to dict reordering
# TODO: Add pickle to store binary data (can be swapped by json)
# TODO: Add OOP members transaction, block, verification, node
# TODO: Add OOP create a printable helper class to output class __repr__

genesis_block = {
    "previous_hash": "GENESIS_BLOCK",
    "index": 0,
    "transactions": [],
}
blockchain_location_path = "blockchain.txt"
owner = "Marc"
participants = set([owner])
blockchain = []
open_transaction = []
MINING_TRANSACTION = 5


def controller():
    """Groupe transaction handler"""
    global participants
    global open_transaction
    global blockchain

    while True:
        user_operation_help = """
            Please choose
            1: Add new transaction
            2: Output blockchain
            3: Mind
            4: Participants
            5: Open transactions
            6: Balance
            q: To Quit
        """
        user_choice, choice_list = get_user_choice(user_operation_help)

        if user_wants_to_quit(user_choice):
            break
        elif user_wants_to_add_a_new_transaction(user_choice):
            transaction_data = get_user_transaction()
            amount, recipient = transaction_data
            add_transaction(recipient, amount=amount)
        elif user_wants_to_output_the_blockchain(user_choice):
            output_blockchain(blockchain)
        elif user_wants_to_mind_new_block(user_choice):
            mine_block(blockchain, open_transaction)
        elif user_wants_to_output_open_transaction(user_choice):
            output_open_transactions(open_transaction)
        elif user_wants_to_output_participants(user_choice):
            output_participant(participants)
        elif user_wants_to_output_balance(user_choice):
            output_user_balance(owner)
        # choice not handled
        elif user_choice not in choice_list:
            print("Input invalid, please choose a listed choice")
        else:
            # choice quit
            break


def save_blockchain(blockchain, open_transaction):
    global blockchain_location_path
    try:
        with open(blockchain_location_path, encoding="utf-8", mode="w") as f:
            data = json.dumps(
                {
                    "blockchain": blockchain,
                    "open_transaction": open_transaction,
                },
                indent=4,
            )
            f.write(data)
    except IOError:
        logger('can\'t write to file {}.'.format(blockchain_location_path))


def load_blockchain(blockchain_location_path):
    global blockchain
    global open_transaction
    file_exists = os.path.exists(blockchain_location_path)
    if not file_exists:
        create_blockchain_file_store(blockchain_location_path)
    hydrate_blockchain(blockchain_location_path)
    if len(blockchain) == 0:
        logger("Init blockchain")
        blockchain.append(genesis_block)

def hydrate_blockchain(blockchain_location_path):
    global blockchain
    global open_transaction
    try:
        with open(blockchain_location_path, encoding="utf-8", mode="r") as f:
            data = json.load(f)
            blockchain = data["blockchain"]
            open_transaction = data["open_transaction"]
    except IOError:
        logger("Can't read the blockchain filestore {}".format(blockchain_location_path))
    except ValueError:
        logger("{} parse failed, file format incorrect.".format(blockchain_location_path))
    return blockchain, open_transaction


def create_blockchain_file_store(blockchain_location_path):
    global blockchain
    global open_transaction
    try:
        with open(blockchain_location_path, encoding="utf-8", mode="w"):
            save_blockchain(blockchain, open_transaction)
    except IOError:
        logger("Can't create the file {}".format(blockchain_location_path))


def verify_chain(blockchain):
    """Verify the blockchain integrity"""
    block_index = -1
    is_valid = True
    compute_previous_hash = ""
    for current_block in blockchain:
        block_index = block_index + 1
        prev_index = block_index - 1
        if _blockchain_has_zero_or_one_block(blockchain):
            break
        if _is_first_block(block_index):
            # skip verification
            continue
        prev_block = blockchain[prev_index]
        prev_block_prev_hash = prev_block["previous_hash"]
        hash_to_check = current_block["previous_hash"]
        salt = current_block["salt"]
        # salt = find_block_salt(current_block['transactions'], prev_block_prev_hash) #debug
        compute_previous_hash = hash_block(
            current_block["transactions"], prev_block_prev_hash, salt
        )

        if compute_previous_hash != hash_to_check:
            is_valid = False
            break
    return (is_valid, block_index)


def _is_first_block(block_index):
    return block_index == 0


def _blockchain_has_zero_or_one_block(blockchain):
    return len(blockchain) <= 1


def reset_blockchain():
    """Wipe the blockchain"""
    global blockchain
    blockchain = []


def get_last_blockchain_value(givin_blockchain=None):
    """Get the last element in the blockchain"""
    global genesis_block
    global blockchain
    used_blockchain = blockchain if givin_blockchain == None else givin_blockchain
    return used_blockchain[-1] if len(used_blockchain) > 0 else genesis_block


def get_user_input(msg, append="\n"):
    """Get a user input"""
    output = input(msg + append)
    return output


# TODO: Marc Flavius - fix sender


def add_transaction(recipient, sender="Marc", amount=1.0):
    """Add a Item to the blockchain
    sender: the sender of the coins.
    recipient: the recipient of the coins.
    amount: the given transaction amount
    """
    global open_transaction

    transaction = {
        "sender": sender,
        "recipient": recipient,
        "amount": amount,
    }
    open_transaction.append(transaction)
    participants.add(sender)
    participants.add(recipient)
    save_blockchain(blockchain, open_transaction)


def mine_block(blockchain, open_transaction):
    """Add all open transaction to a block and wipe
    the open transaction array"""
    previous_hash = get_last_blockchain_value(blockchain)["previous_hash"]
    old_blockchain = blockchain[:]
    reward_transaction = {
        "sender": "MINING",
        "recipient": owner,
        "amount": MINING_TRANSACTION,
    }
    open_transaction.append(reward_transaction)
    # hashing
    salt = find_block_salt(open_transaction, previous_hash)
    current_hash = hash_block(open_transaction, previous_hash, salt)
    new_block = {
        "previous_hash": current_hash,
        "index": len(blockchain),
        "transactions": open_transaction[:],
        "salt": salt,
    }
    blockchain.append(new_block)

    valid, index = verify_chain(blockchain)
    if valid:
        save_blockchain(blockchain, [])
        open_transaction.clear()
        logger("Block added!")
    else:
        # revert
        revert_chain(blockchain, old_blockchain)
        logger("Invalid chain! at index {}".format(index))


def revert_chain(blockchain, old_blockchain):
    blockchain.clear()
    for block in old_blockchain:
        blockchain.append(block)


def logger(msg):
    print(msg)


def hash_block(open_transaction, previous_hash, salt):
    return hash.sha256(
        stringify_decoded_hash(open_transaction, previous_hash, salt)
    ).hexdigest()


def get_user_transaction():
    """Get user input transaction"""
    recipient = (
        "" + get_user_input("Enter the recipient of the transaction: ")
    ).capitalize()
    tx_amount = get_numeric_input("Your transaction please: ")
    return tx_amount, recipient


def get_numeric_input(input):
    tx_amount = input
    match = len(re.findall("[0-9]+$", tx_amount))
    if match != 1:
        print("Please enter a numeric amount\n")
        tx_amount = get_numeric_input(get_user_input(input))
    return int(tx_amount)


def get_user_choice(user_operation_help):
    """Get user choice"""
    choice_list = re.findall("[0-9-q]+(?=:)", user_operation_help)
    user_choice = get_user_input(user_operation_help)
    return (
        user_choice,
        choice_list,
    )


def user_wants_to_quit(user_choice):
    return user_choice == "q"


def user_wants_to_add_a_new_transaction(user_choice):
    """Check for a new transaction operation"""
    return str(user_choice) == "1"


def user_wants_to_output_the_blockchain(user_choice):
    """Check for a output blockchain operation"""
    return str(user_choice) == "2"


def user_wants_to_mind_new_block(user_choice):
    return str(user_choice) == "3"


def user_wants_to_output_participants(user_choice):
    return str(user_choice) == "4"


def user_wants_to_output_open_transaction(user_choice):
    return str(user_choice) == "5"


def user_wants_to_output_balance(user_choice):
    return str(user_choice) == "6"


def output_blockchain(given_blockchain):
    """Output the block chain"""
    for block in given_blockchain:
        print("Outputting block...")
        print(block)


def output_participant(participants):
    print(participants)
    return participants


def output_open_transactions(open_transactions):
    print(open_transactions)
    return open_transaction


def get_user_balance(user_id):
    global blockchain
    last_block = get_last_blockchain_value()
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


def output_user_balance(user_id):
    balance = get_user_balance(user_id)
    print(balance)
    return balance


def valid_salt(open_transaction, previous_hash, salt):
    guess = stringify_decoded_hash(open_transaction, previous_hash, salt)
    guess_hash = hash.sha256(guess).hexdigest()
    return guess_hash[0:1] == "0"


def stringify_decoded_hash(open_transaction, previous_hash, salt):
    return (str(open_transaction) + str(previous_hash) + str(salt)).encode()


def find_block_salt(transactions, previous_hash):
    """_summary_

    Args:
        transactions (list): open transaction
        previous_hash (str): previous hash stored on last block in the chain

    Returns:
        _type_: int
    """
    salt = -1
    valid = False
    while valid is not True:
        salt = salt + 1
        valid = valid_salt(transactions, previous_hash, salt)
    return salt


def main():
    global blockchain_location_path

    load_blockchain(blockchain_location_path)
    controller()
    logger("God Bye!")


if __name__ == "__main__":
    main()
