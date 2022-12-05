import re

from log import Log
from blockchain import Blockchain

class Node():
    def __init__(self, blockchain, owner):
            self.blockchain = blockchain
            self.owner = owner

    """ User interface """
    def controller(self):
        """Groupe transaction handler"""
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
            user_choice, choice_list = Node.get_user_choice(user_operation_help)

            if Node.user_wants_to_quit(user_choice):
                break
            elif Node.user_wants_to_add_a_new_transaction(user_choice):
                transaction_data = Node.get_user_transaction()
                amount, recipient = transaction_data
                self.add_transaction(recipient, amount=amount)
            elif self.user_wants_to_output_the_blockchain(user_choice):
                self.blockchain.output_blockchain(self.blockchain.blockchain)
            elif self.user_wants_to_mind_new_block(user_choice):
                self.blockchain.mine_block(self.blockchain.blockchain, self.blockchain.open_transaction)
            elif self.user_wants_to_output_open_transaction(user_choice):
                self.blockchain.output_open_transactions(self.blockchain.open_transaction)
            elif self.user_wants_to_output_participants(user_choice):
                self.blockchain.output_participant(self.blockchain.participants)
            elif self.user_wants_to_output_balance(user_choice):
                self.blockchain.output_user_balance(self.owner)
            # choice not handled
            elif user_choice not in choice_list:
                print("Input invalid, please choose a listed choice")
            else:
                # choice quit
                break
    @staticmethod
    def get_user_input(msg, append="\n"):
        """Get a user input"""
        output = input(msg + append)
        return output
    @staticmethod
    def get_user_transaction():
        """Get user input transaction"""
        recipient = (
            "" + Node.get_user_input("Enter the recipient of the transaction: ")
        ).capitalize()
        tx_amount = Node.get_numeric_input("Your transaction please: ")
        return tx_amount, recipient

    @staticmethod
    def get_numeric_input(input):
        tx_amount = input
        match = len(re.findall("[0-9]+$", tx_amount))
        if match != 1:
            print("Please enter a numeric amount\n")
            tx_amount = Node.get_numeric_input(Node.get_user_input(input))
        return int(tx_amount)

    @staticmethod
    def get_user_choice(user_operation_help):
        """Get user choice"""
        choice_list = re.findall("[0-9-q]+(?=:)", user_operation_help)
        user_choice = Node.get_user_input(user_operation_help)
        return (
            user_choice,
            choice_list,
        )
    
    @staticmethod
    def user_wants_to_quit(user_choice):
        return user_choice == "q"

    @staticmethod
    def user_wants_to_add_a_new_transaction(user_choice):
        """Check for a new transaction operation"""
        return str(user_choice) == "1"

    @staticmethod
    def user_wants_to_output_the_blockchain(user_choice):
        """Check for a output blockchain operation"""
        return str(user_choice) == "2"

    @staticmethod
    def user_wants_to_mind_new_block(user_choice):
        return str(user_choice) == "3"

    @staticmethod
    def user_wants_to_output_participants(user_choice):
        return str(user_choice) == "4"

    @staticmethod
    def user_wants_to_output_open_transaction(user_choice):
        return str(user_choice) == "5"

    @staticmethod
    def user_wants_to_output_balance(user_choice):
        return str(user_choice) == "6"

    def main(self):
        self.blockchain.load_blockchain(self.blockchain.blockchain_location_path)
        self.controller()
        Log.log("God Bye!")

    def add_transaction(self, recipient, sender="Marc", amount=1.0):
        """Add a Item to the blockchain
        sender: the sender of the coins.
        recipient: the recipient of the coins.
        amount: the given transaction amount
        """
        transaction = {
            "sender": sender,
            "recipient": recipient,
            "amount": amount,
        }
        self.blockchain.open_transaction.append(transaction)
        self.blockchain.participants.add(sender)
        self.blockchain.participants.add(recipient)
        self.blockchain.save_blockchain(self.blockchain.blockchain, self.blockchain.open_transaction)

if __name__ == "__main__":
    blockchain = Blockchain('Marc')
    node = Node(blockchain, blockchain.owner)
    node.main()
