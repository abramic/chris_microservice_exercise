import os
import requests
from json import dumps
from pymongo import MongoClient

import decorators
import errors

class Database(object):
    def __init__(self):
        self.client = MongoClient(os.getenv('MONGO_ATLAS_CONNECTION_STRING'))
        self.db = self.client['yelp_api_backend_db']
        self.collection = self.db['restaurant_info']

    def find_one(self, user_id):
        try:
            result = self.collection.find_one({'user_id': str(user_id)})
            return result
        except Exception as e:
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