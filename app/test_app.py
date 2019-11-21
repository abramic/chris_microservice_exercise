from app import app
import unittest
from json import loads
# To run this, run the following command (inside the app folder):  
# python3 -m unittest test_app.py

# Also, in the flask app, just have app.run() with no port or debug options

# Response data has to be parsed.  Also, if data comes back as string, it comes back as
# a byte string, with 'b' affixed to the front of it


class TestMyApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_one(self):
        rv = self.app.get('/')
        assert rv.status == '200 OK'

    def test_two(self):
        rv = self.app.get('/')
        # print('RESPONSE DATA IS', rv.data)
        # print('LOADS DATA IS', loads(rv.data))
       
        self.assertEqual(loads(rv.data), {"prop": "Hello World!"})

    def test_three(self):
        rv = self.app.get('/')
        self.assertEqual(loads(rv.data), {"prop": "Hello Globe!"})




if __name__ == "__main__":
    unittest.main()