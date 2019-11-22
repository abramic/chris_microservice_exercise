from app import app
import unittest
from json import loads
# import inspect

# Look into mock and patch

# The method definition MUST have test in the name, in order for the testing suite to run it as a test

# Our tests appear to be a subclass of the unittest.TestCase class, which I think has an app prop already set on
# it, which is why we can reference self.app

# To run this, run the following command (inside the app folder):  
# python3 -m unittest test_app.py -v

# State managed inside the class has to be declared as a mutable type (a list or dictionary) so that it can be changed if by tests and 
# referenced by later tests

# The server should start up, and it'll just look like nothing's hitting it.  Let it run for 
# a time and then stop it with Control+C.  The results of only the non passing tests should
# show up.  The -v flag means 'verbose' - it'll show you also the tests that pass AND will show you the console,
# as if you were looking at the console while doing manual testing from Postman

# The order of arguments in a POST/PATCH should be URL, followed by the json={whatever it is}
# Doesn't seem to have to be 'dumped' into JSON ahead of time

# Also, in the flask app, just have app.run() with no port or debug options

# Response data has to be parsed.  Also, if data comes back as string, it comes back as
# a byte string, with 'b' affixed to the front of it
# Class methods get executed in order



class TestServer(unittest.TestCase):
    # These have to be a mutable type so that the respective test functions can mutate them as need be
    user_id = []

    def setUp(self):
        self.app = app.test_client()

    def test_create_user(self):
        print('TEST_CREATE_USER')
        rv = self.app.post('/users?user_name=test_suite_user')
        response_data = loads(rv.data)
        assert rv.status == '201 CREATED'
        assert type(response_data).__name__ == 'dict'
        assert response_data.get('id', None) is not None
        # print(response_data)
        id = response_data.get('id')
        self.user_id.append(id)
        # print('ID is', id)
        # self.user_id = id

    def test_successfully_add_location(self):
        print('TEST CREATE USER TWO')
        # print('USER ID', self.user_id)
        payload = {
            "location": "new_york",
            "latitude": 40.785091,
            "longitude": -73.968285
        }

        print('USER ID', self.user_id)
        rv = self.app.patch(f'/locations?user_id={self.user_id[0]}', json=payload)
        assert rv.status == '201 CREATED'
        




if __name__ == "__main__":
    unittest.main()