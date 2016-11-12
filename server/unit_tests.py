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

if __name__ == '__main__':
    unittest.main()
