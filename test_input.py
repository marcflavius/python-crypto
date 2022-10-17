import unittest
from unittest.mock import patch
from unittest import TestCase
import blockchain

def get_input(text):
    return input(text)


def answer():
    ans = blockchain.get_user_input('enter yes or no')
    if ans == 'yes':
        return 'you entered yes'
    if ans == 'no':
        return 'you entered no'


class Test(TestCase):

    # get_input will return 'yes' during this test
    @patch('blockchain.get_user_input', return_value='yes')
    def test_answer_yes(self, input):
        self.assertEqual(answer(), 'you entered yes')

    # @patch('yourmodule.get_input', return_value='no')
    # def test_answer_no(self, input):
        # self.assertEqual(answer(), 'you entered no')



if __name__ == '__main__':
    unittest.main()
