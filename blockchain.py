""" Blockchain lib """
blockchain = []


def get_last_blockchain_value():
    """ Get the last element in the blockchain"""
    return blockchain[-1]


def get_user_input_func(msg):
    """ Get a user input """
    return float(input(msg+': \n'))


def add_value_func(transaction_amount, last_transaction=[1]):
    """ Add a Item to the blockchain """
    blockchain.append([last_transaction, transaction_amount])
    print(blockchain)


def grouped_transaction(get_user_input, add_value):
    """ Groupe transaction handler"""
    total_transaction = int(get_user_input("Please enter the number of transaction you wish to proceed"))
    for count in range(total_transaction):
        tx_amount = get_user_input('{}/{} Your transaction please: '.format(count+1, total_transaction))
        add_value(tx_amount)


grouped_transaction(get_user_input_func, add_value_func)


print(blockchain)
print('God Bye!')
