import os
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.temp = "temp"

    def test_temp(self):
        assert self.temp == "temp"

    def tearDown(self):
        self.temp = None

if __name__ == '__main__':
    unittest.main()
