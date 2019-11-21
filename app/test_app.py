from app import app
import unittest
from json import loads

# The method definition MUST have test in the name, in order for the testing suite to run it as a test

# To run this, run the following command (inside the app folder):  
# python3 -m unittest test_app.py

# The server should start up, and it'll just look like nothing's hitting it.  Let it run for 
# a time and then stop it with Control+C.  The results of only the non passing tests should
# show up

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

    # def test_three(self):
    #     rv = self.app.get('/')
    #     self.assertEqual(loads(rv.data), {"prop": "Hello Globe!"})

    def test_four(self):
        rv = self.app.get('/locations?user_id=5dd46e6ec2dddbebad4078b6')
        body = loads(rv.data)
        print('THE BODY IS: ', body)
        self.assertEqual(rv.status, '404 OK')

if __name__ == "__main__":
    unittest.main()