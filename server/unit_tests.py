import unittest
from sentences import Lexicon

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

if __name__ == '__main__':
    unittest.main()
