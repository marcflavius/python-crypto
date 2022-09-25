""" Blockchain lib """
blockchain = []


def get_last_blockchain_value():
    """ Get the last element in the blockchain"""
    return blockchain[-1] if len(blockchain) > 0 else [1]


def get_user_input(msg):
    """ Get a user input """
    return float(input(msg+': \n'))


def add_value(transaction_amount, last_transaction):
    """ Add a Item to the blockchain """
    blockchain.append([last_transaction, transaction_amount])


def grouped_transaction():
    """ Groupe transaction handler"""
    total_transaction = int(get_user_input("Please enter the number of transaction you wish to proceed"))
    for count in range(total_transaction):
        tx_amount = get_user_input('{}/{} Your transaction please: '.format(count+1, total_transaction))
        add_value(tx_amount, get_last_blockchain_value())


grouped_transaction()


for block in blockchain:
    print('Outpouting blck')
    print(block)
print('God Bye!')
