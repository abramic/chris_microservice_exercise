import os
import requests
import bson

from json import dumps
from pymongo import MongoClient, errors as mongo_errors
from bson.objectid import ObjectId
from functools import wraps

import decorators
import errors

# TO DO:  Potentially move all these subclasses out of Database and make everything a database class
class Database(object):
    def __init__(self):
        self.client = MongoClient(os.getenv('MONGO_ATLAS_CONNECTION_STRING'))
        self.db = self.client['yelp_api_backend_db']
        self.collection = self.db['restaurant_info']


class User(Database):
    def __init__(self, user_name):
        super().__init__()

        self.new_user_structure = {
            'user_name': user_name,
            'locations': {},
            'restaurants': []
        }


    @decorators.print_func_name()
    @decorators.handle_mongo_errors()
    def insert_new_user(self):
        response = 'Empty'
        data = self.new_user_structure
        result = self.collection.insert_one(data)
        if result is None:
            raise errors.DatabaseUserInsertion()
        else:
            return {
                'id': str(result.inserted_id)
            }
        return response


class Restaurants(Database):
    def __init__(self):
        super().__init__()


    @decorators.print_func_name()
    # @decorators.handle_mongo_errors()
    def check_if_at_least_one_restaurant(self, user_id):
        result = self.collection.find_one({
                '_id': ObjectId(user_id)
            },{
                'restaurants': 1
            }
        )
        restaurants = result.get('restaurants', None)
        if len(restaurants) == 0: 
            return False
        else:
            return True


    # TO DO - Expand error handling capabilities on such functions, right now we're just returning if we get that far
    @decorators.print_func_name()
    @decorators.handle_mongo_errors()
    def insert_restaurants(self, user_id, restaurants):
            response = self.collection.update({
                '_id': ObjectId(user_id),
                },
                {
                    "$set": {
                        "restaurants": restaurants
                    }
                }
            )
            return {}


    @decorators.print_func_name()
    @decorators.handle_mongo_errors()
    def retrieve_page_of_restaurants(self, user_id, limit, offset):
        response = self.collection.find({
            '_id': ObjectId(user_id),
            },
            {
                "restaurants": { 
                    "$slice": [ offset , limit ]
                }  
            },
        )
        restaurants = response[0]['restaurants']
        second_response = self.collection.find({
            '_id': ObjectId(user_id),
            },
            {
                "restaurants": 1 
            },
        )   
        length = len(second_response[0]['restaurants'])
        return {
            'restaurants': restaurants,
            'total': length
        }


class Locations(Database):
    def __init__(self):
        super().__init__()
              

    @decorators.print_func_name()  
    @decorators.handle_mongo_errors()
    def insert_new_location(self, user_id, body):
        record_object_id = ObjectId()
        response = self.collection.update({
            '_id': ObjectId(user_id),
            },
            {
                "$set": {
                    f"locations.{record_object_id}": body
                }
            }
        )
        return {
            'id': str(record_object_id)
        }
            


    @decorators.print_func_name()
    @decorators.handle_mongo_errors()
    def update_location(self, user_id, location_id, body):
        base_set_path = f"locations.{location_id}"
        set_object = {}
        for key in body.keys():
            set_object[f"{base_set_path}.{key}"] = body.get(key)
        response = self.collection.update({
            '_id': ObjectId(user_id),
            },
            {
                "$set": set_object
            }
        )
        return {
            'id': location_id,
        }



    @decorators.print_func_name() 
    @decorators.handle_mongo_errors()
    def retrieve_all_locations(self, user_id):
        result = self.collection.find_one({
                '_id': ObjectId(user_id)
            },{
                'locations': 1
            }
        )
        locations = result.get('locations', None)
        if locations is None: raise errors.NoLocationsForThisUser()
        return locations



    @decorators.print_func_name()  
    @decorators.handle_mongo_errors()
    def check_if_at_least_one_location(self, user_id):
        # print(os.getenv('MONGO_ATLAS_CONNECTION_STRING'))
        result = self.collection.find_one({
                '_id': ObjectId(user_id)
            },{
                'locations': 1
            }
        )
        locations = result.get('locations', None)
        if locations is None or len(locations) == 0: raise errors.NoLocationsForThisUser()
        return locations


class Yelp(object):
    def __init__(self, token=os.getenv('YELP_BEARER_TOKEN')):
        self.token = token


    @decorators.print_func_name()
    @decorators.retry_func(retries=5)
    def get(self, parameters):
        response = requests.get(
            'https://api.yelp.com/v3/businesses/search',
            parameters,
            headers={
                'authorization': self.token
            }
        )
        if response.status_code != 200:
            if response.status_code == 429:
                raise errors.YelpConcurrencyError()
        return response.json()
