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
    location_id = []

    def setUp(self):
        self.app = app.test_client()


    def test_create_user(self):
        rv = self.app.post('/users?user_name=test_suite_user')
        response_data = loads(rv.data)
        assert rv.status == '201 CREATED'
        assert type(response_data).__name__ == 'dict'
        assert response_data.get('id', None) is not None
        id = response_data.get('id')
        self.user_id.append(id)


    def handler_errors(self, resp, message, exp_error_code):
        self.assertEqual(resp.status, message) 
        rb = loads(resp.data)
        rb_type = type(rb).__name__
        self.assertNotEqual(rb, None)
        self.assertEqual(rb_type, 'dict')
        error_code = rb.get('error_code', None)
        self.assertNotEqual(error_code, None)
        self.assertEqual(error_code, exp_error_code)


# Test try GETing restuarants for a user when no 
# location have been entered
    
    
    def test_restaurants_without_locations(self):
        resp = self.app.get(f'/restaurants?user_id={self.user_id[0]}')
        self.handler_errors(resp, '400 BAD REQUEST', 606)


# Locations


    def test_location_without_user_id(self):
        payload = {
            "location": "new_york",
            "latitude": 40.785091,
            "longitude": -73.968285
        }
        resp = self.app.patch(f'/locations', json=payload)
        self.handler_errors(resp, '400 BAD REQUEST', 701)

# This should actually be a 605 error
    def test_location_with_user_id_not_in_db(self):
        payload = {
            "location": "new_york",
            "latitude": 40.785091,
            "longitude": -73.968285
        }
        resp = self.app.patch(f'/locations?user_id=NonexistentUser', json=payload)
        self.handler_errors(resp, '400 BAD REQUEST', 600)


    def test_location_new_incorrect_method(self):
        # We're hitting with POST, should be hitting with PATCH
        payload = {
            "location": "new_york",
            "latitude": 40.785091,
            "longitude": -73.968285
        }
        resp = self.app.post(f'/locations', json=payload)
        self.handler_errors(resp, '405 METHOD NOT ALLOWED', 405)
 
 
    def test_location_new_with_incorrect_structure(self):
        payload = [{
            "location": "new_york",
            "latitude": 40.785091,
            "longitude": -73.968285
        }]
        resp = self.app.patch(f'/locations?user_id={self.user_id[0]}', json=payload)
        self.handler_errors(resp, '400 BAD REQUEST', 801)


    def test_location_new_with_unallowed_property(self):
        payload = {
            "location": "new_york",
            "latitude": 40.785091,
            "longitude": -73.968285,
            "incorrect": "property" 
        }
        resp = self.app.patch(f'/locations?user_id={self.user_id[0]}', json=payload)
        self.handler_errors(resp, '400 BAD REQUEST', 804)


    def test_location_new_with_missing_required_props(self):
        payload = {
            # "location": "new_york", location is a required field
            "latitude": 40.785091,
            "longitude": -73.968285,
        }
        resp = self.app.patch(f'/locations?user_id={self.user_id[0]}', json=payload)
        self.handler_errors(resp, '400 BAD REQUEST', 803) 


    def test_location_if_prop_is_wrong_type(self):
        payload = {
            "location": "new_york",
            "latitude": [40.785091], #should not be a list
            "longitude": -73.968285,
        }
        resp = self.app.patch(f'/locations?user_id={self.user_id[0]}', json=payload)
        self.handler_errors(resp, '400 BAD REQUEST', 802) 


    def test_successfully_add_location(self):
        payload = {
            "location": "new_york",
            "latitude": 40.785091,
            "longitude": -73.968285
        }
        resp = self.app.patch(f'/locations?user_id={self.user_id[0]}', json=payload)
        self.assertEqual(resp.status, '201 CREATED') 
        rb = loads(resp.data)
        rb_type = type(rb).__name__
        self.assertNotEqual(rb, None)
        self.assertEqual(rb_type, 'dict')
        id = rb.get('id', None)
        self.assertNotEqual(id, None)
        self.location_id.append(id)


    def test_location_modified_incorrect_method(self):
        # We're hitting with PUT, should be hitting with PATCH
        payload = {
            "location": "new_york_city",
            "latitude": 40.785091,
            "longitude": -73.968285
        }
        resp = self.app.put(f'/locations', json=payload)
        self.handler_errors(resp, '405 METHOD NOT ALLOWED', 405)


    def test_successfully_modify_location(self):
        payload = {
            "location": "new_york_city"
        }
        resp = self.app.patch(f'/locations?user_id={self.user_id[0]}&location_id={self.location_id[0]}', json=payload)
        self.assertEqual(resp.status, '204 NO CONTENT')
  

    def test_unsuccessfully_modify_location(self):
        payload = {
            "location": ["new_york_city"]
        }
        resp = self.app.patch(f'/locations?user_id={self.user_id[0]}&location_id={self.location_id[0]}', json=payload)
        self.handler_errors(resp, '400 BAD REQUEST', 802) 


# Restaurants


    def test_restaurants_method_not_allowed(self):
        # Should be 'GET'
        resp = self.app.patch(f'/restaurants')
        self.handler_errors(resp, '405 METHOD NOT ALLOWED', 405)


    def test_restaurants_require_user_id(self):
        resp = self.app.get(f'/restaurants')
        self.handler_errors(resp, '400 BAD REQUEST', 701)

    
  





    





if __name__ == "__main__":
    unittest.main()



   
   
