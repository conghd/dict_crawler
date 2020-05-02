import random
import unittest
from reader import Reader
from writer import Writer

class ReaderTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_read(self):
        filename = 'input.txt'
        words = Reader.read(filename)

        self.assertEqual(words[0], 'utter')
        self.assertEqual(words[1], 'mean')
        self.assertEqual(words[2], 'detrimental')

    def tearDown(self):
        pass

class WriterTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_write(self):
        filename = "test_write_%s.txt" % (random.randrange(1000))
        words = ['comtemporary', 'advanced']
        Writer.write(filename, words)

        # Read
        output_words = Reader.read(filename)
        self.assertEqual(words[0], words[-2])
        self.assertEqual(words[1], words[-1])

if __name__ == '__main__':
        unittest.main()
