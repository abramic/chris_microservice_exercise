import os
import requests
from json import dumps
from pymongo import MongoClient
from bson.objectid import ObjectId

import decorators
import errors

class Database(object):
    def __init__(self):
        self.client = MongoClient(os.getenv('MONGO_ATLAS_CONNECTION_STRING'))
        self.db = self.client['yelp_api_backend_db']
        self.collection = self.db['restaurant_info']

    # def find_one(self, user_id):
    #     try:
    #         result = self.collection.find_one({'user_id': str(user_id)})
    #         return result
    #     except Exception as e:
    #         raise e

class User(Database):
    def __init__(self, user_name):
        super().__init__()

        self.new_user_structure = {
            'user_name': user_name,
            'locations': {},
            'restaurants': {}
        }

    @decorators.print_func_name()
    def insert_new_user(self):
        try:
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
        except Exception as e:
            print(e)
            raise e


class Restaurants(Database):
    def __init__(self):
        super().__init__()

    @decorators.print_func_name()
    def insert_new_restaurants_for_user(self, data):
        try:
            result = self.collection.insert_one(data)
            if result is None:
                raise errors.RestaurantGetRequestInsertion()
            else:
                insertion_id = result.inserted_id
                response = {
                    'insertion_id': str(insertion_id)
                }
                return response
        except Exception as e:
            raise e


class Locations(Database):
    def __init__(self):
        super().__init__()
        self.location_structure = {
            "location_name": None,
            "latitude": None,
            "longitude": None
        }

    # def generate_location_id = {
      
    # }


    @decorators.print_func_name()   
    def insert_new_location(self, user_id, body):
        # for now, just use default location structure
        print(user_id, body)
        try: 
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
            print(response)
            # TO DO: Add additional validation and error handling on response body
            return {
                'id': str(record_object_id)
            }
        except Exception as e:
            raise errors.DatabaseLocationInsertion(e)

    def insert_for_existing_user():
        pass
    


class Yelp(object):
    def __init__(self, token=os.getenv('YELP_BEARER_TOKEN')):
        self.token = token

    @decorators.print_func_name()
    @decorators.retry_func(retries=5)
    def get(self, parameters):
        try:
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
        except Exception as e:
            raise e