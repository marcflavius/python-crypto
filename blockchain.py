
blockchain = []


def get_last_blockchain_value():
    return blockchain[-1]

def get_user_input(msg):
    return float(input(msg+': \n'))
    
def add_value(transaction_amount, last_transaction=[1]):
    blockchain.append([last_transaction, transaction_amount])
    print(blockchain)


tx_amount = get_user_input('Your transaction please: ')
add_value(tx_amount)
tx_amount = get_user_input('Your transaction please: ')
add_value(tx_amount)
tx_amount = get_user_input('Your transaction please: ')
add_value(tx_amount)


print(blockchain)