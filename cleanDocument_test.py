import unittest
from main import capitalizeSentences

class TestStringMethods(unittest.TestCase):

    def test_capitalizeSentences(self):
        input_list = [
            'This is a really simple test',
            'THIS IS THE BEST TEST OF THE WORLD',
            'nothing can be seen in here',
            'do you like chocolate and banana?'
        ]
        output_list = [
            'This Is a Really Simple Test',
            'This Is The Best Test of The World',
            'Nothing Can Be Seen in Here',
            'Do You Like Chocolate and Banana?'
        ]
        for i in range(len(input_list)):
            self.assertEqual(capitalizeSentences(input_list[i]), output_list[i])

if __name__ == '__main__':
    unittest.main()