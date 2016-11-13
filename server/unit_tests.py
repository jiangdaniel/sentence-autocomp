import unittest
from sentences import Lexicon
from sentences import VariableSentence

from app import app


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_temp(self):
        temp = "temp"
        self.assertEqual(temp, "temp")
        self.assertNotEqual(temp, "not temp")
        self.assertTrue(True)
        self.assertFalse(False)

    def tearDown(self):
        pass

class HomeTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client(self)

    def test_home(self):
        rv = self.app.get('/')
        self.assertEqual(rv.status_code, 200)
        self.assertTrue(b'Hello World!' in rv.data)

class PostTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client(self)

    def test_post(self):
        text = b'Testing our handling of post requests'
        rv = self.app.post('/js', data={'text': text})
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(text, rv.data)

class LexiconTestCase(unittest.TestCase):
    def setUp(self):
        file_path = '../scikit/sample_text.txt'
        self.file = open(file_path, 'r')

    def test_post(self):
        lexicon = Lexicon()
        lexicon.add_text(self.file.read())
        self.file.close()

class TrainTestCase(unittest.TestCase):
    def setUp(self):
        file_path = '../scikit/sample_text.txt'
        self.file = open(file_path, 'r')
        self.app = app.test_client(self)

    def test_post(self):
        rv = self.app.post('/train', data={'text': self.file.read()})
        self.assertEqual(rv.status_code, 200)
        # FIXME: actually should assert something
        # print(rv.data)

    def tearDown(self):
        self.file.close()

class ConstructTreeTestCase(unittest.TestCase):
    def setUp(self):
        self.lexicon = Lexicon()
        self.sentences = ['The cat in the hat', 'The cat plays piano', 'The dog drives up the road', 'Where is my mind']
        for sentence in self.sentences:
            self.lexicon._add_sentence(sentence)

    def test_post(self):
        trie = self.lexicon.construct_trie()
        for sentence in self.sentences:
            curr_trie = trie
            words = sentence.split()
            for word in words:
                self.assertTrue(curr_trie.has_child(word))
                curr_trie = curr_trie.get_child(word)

    def tearDown(self):
        pass

class VarSentenceTestCase(unittest.TestCase):
    def setUp(self):
        self.variations1 = [
        'The quick brown fox jumps over the lazy dog and cat',
        'The quick red fox jumps over the happy dog',
        'The quick green fox jumps over the sad dog',
        'The quick purple fox jumps over the cheering dog',
        'The quick orange fox jumps over the lazy dog',
        'The quick brown fox jumps over the lazy dog'
        ]
        self.correct1 = 'The quick %s fox jumps over the %s dog %s'
        self.variations2 = [
        'A quick brown fox jumps over the lazy dog',
        'The quick brown fox jumps over the lazy dog',
        'My quick brown fox jumps over the lazy dog',
        'Your quick brown fox jumps up over the lazy dog',
        'The quick brown fox jumps up and over the lazy dog',
        'The quick brown fox jumps over the lazy dog'
        ]
        self.correct2 = '%s quick brown fox jumps %s over the lazy dog'

    def test_create(self):
        self.assertEqual(self.correct1, VariableSentence.create(self.variations1).data)
        self.assertEqual(self.correct2, VariableSentence.create(self.variations2).data)


class TrieTestCase(unittest.TestCase):
    def setUp(self):
        self.lexicon = Lexicon()
        self.lexicon.add_text("Thanks for the update. I do not have an apple. Thanks for the update. You can collect them all. Thanks for the update. Zero is the loneliest number. Thanks for the update. I'll see you at 2. I'll see you at two. I'll see you at three o'clock. I'll see you at the end. I'll see you later. The woods are lovely dark and deep.")
        self.trie = self.lexicon.construct_trie()

    def test_child(self):
        self.assertIsNotNone(self.trie.random_child())

    def test_complete(self):
        self.assertEqual(self.lexicon.complete("Thanks for"), "the update")

if __name__ == '__main__':
    unittest.main()
