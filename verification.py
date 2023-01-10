import hashlib as hash


class Verification:
    @staticmethod
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
            valid = Verification.valid_salt(transactions, previous_hash, salt)
        return salt

    @staticmethod
    def valid_salt(open_transaction, previous_hash, salt):
        guess = Verification.stringify_decoded_hash(
            open_transaction, previous_hash, salt
        )
        guess_hash = hash.sha256(guess).hexdigest()
        return guess_hash[0:1] == "0"

    @staticmethod
    def stringify_decoded_hash(open_transaction, previous_hash, salt):
        return (str(open_transaction) + str(previous_hash) + str(salt)).encode()

    @staticmethod
    def hash_block(open_transaction, previous_hash, salt):
        return hash.sha256(
            Verification.stringify_decoded_hash(open_transaction, previous_hash, salt)
        ).hexdigest()

    @staticmethod
    def _is_first_block(block_index):
        return block_index == 0

    @staticmethod
    def _blockchain_has_zero_or_one_block(blockchain):
        return len(blockchain) <= 1

    @staticmethod
    def verify_chain(blockchain):
        """Verify the blockchain integrity"""
        block_index = -1
        is_valid = True
        compute_previous_hash = ""
        for current_block in blockchain:
            block_index = block_index + 1
            prev_index = block_index - 1
            if Verification._blockchain_has_zero_or_one_block(blockchain):
                break
            if Verification._is_first_block(block_index):
                # skip verification
                continue
            prev_block = blockchain[prev_index]
            prev_block_prev_hash = prev_block["previous_hash"]
            hash_to_check = current_block["previous_hash"]
            salt = current_block["salt"]
            # salt = find_block_salt(current_block['transactions'], prev_block_prev_hash) #debug
            compute_previous_hash = Verification.hash_block(
                current_block["transactions"], prev_block_prev_hash, salt
            )

            if compute_previous_hash != hash_to_check:
                is_valid = False
                break
        return (is_valid, block_index)
