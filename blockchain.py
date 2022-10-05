""" Blockchain lib """
import pprint

genesis_block = {
    "previous_hash": "",
    "index": 0,
    "transactions": [],
},

owner = "Marc"
blockchain = []
open_transaction = []


def verify_chain():
    """ Verify the blockchain integrity """
    block_index = 0
    is_valid = True
    for current_block in blockchain:
        prev_block = blockchain[block_index - 1]["previous_hash"]
        if current_block != prev_block:
            is_valid = False
            break
    return is_valid if current_block["previous_hash"] == None else True


def reset_blockchain():
    """ Wipe the blockcain """
    global blockchain
    blockchain = []


def get_last_blockchain_value():
    """ Get the last element in the blockchain """
    return blockchain[-1] if len(blockchain) > 0 else None


def get_user_input(msg):
    """ Get a user input """
    output = input(msg+': \n')
    return output


def get_user_input_raw(msg):
    """ Get a user input raw apply no format to the message outputted """
    return input(msg)


def add_transaction(recipient, sender=owner, amount=1.0):
    """ Add a Item to the blockchain 
    sender: the sender of the coins. 
    recipient: the recipient of the coins.
    amount: the given transaction amount
    """
    transaction = {"sender": sender, "recipient": recipient, "amount": amount, }
    open_transaction.append(transaction)


def mine_block():
    """ Add all open transaction to a block and wipe the open transaction arry"""
    global blockchain
    global open_transaction

    last_block = blockchain[-1] if len(blockchain) else None

    previous_hash = last_block
    new_block = {
        "previous_hash": previous_hash,
        "index": len(blockchain),
        "transactions": open_transaction,
    }
    # hashed_block = last_block
    open_transaction = []
    blockchain.append(new_block)


def grouped_transaction(given_blockchain):
    """ Groupe transaction handler """
    while True:
        user_operation_help = """
            Please choose
            1: Add a new transaction value
            2: Output the blockchain blocs
            2: Mind transaction
            q: To Quit
        """
        user_choice, choice_list = get_user_choice(user_operation_help)

        # choice 1
        if user_wants_to_add_a_new_transaction(user_choice):
            transaction_data = get_user_transaction()
            amount, recipient = transaction_data
            add_transaction(recipient, amount=amount)
        # choice 2
        elif user_wants_to_output_the_blockchain(user_choice):
            output_blockchain(given_blockchain)
        # choice not handled
        elif user_choice not in choice_list:
            print('Input invalid, please choose a listed choice')
        else:
            # choice 3
            break


def get_user_transaction():
    """ Get user input transaction"""
    recipient = (get_user_input('Enter the recipient of the transaction: ')).capitalize()
    tx_amount = float(get_user_input('Your transaction please: '))
    return tx_amount, recipient


def get_user_choice(user_operation_help):
    """ Get user choice """
    user_choice = get_user_input_raw(user_operation_help)
    choice_list = [str(item+1) for item in range(2)]
    choice_list.append('q')
    return user_choice, choice_list,


def user_wants_to_output_the_blockchain(user_choice):
    """ Check for a output blockchain operation """
    return str(user_choice) == '2'


def user_wants_to_add_a_new_transaction(user_choice):
    """ Check for a new transaction operation """
    return str(user_choice) == '1'


def output_blockchain(given_blockchain):
    """ Output the block chain """
    for block in given_blockchain:
        print('Outputting block')
        print(block)


if __name__ == "__main__":
    # grouped_transaction(blockchain)
    print('God Bye!')
