import os
import requests
import bson

from json import dumps
from pymongo import MongoClient
from bson.objectid import ObjectId

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

    # @decorators.print_func_name()
    # def insert_new_restaurants_for_user(self, data):
    #     try:
    #         result = self.collection.insert_one(data)
    #         if result is None:
    #             raise errors.RestaurantGetRequestInsertion()
    #         else:
    #             insertion_id = result.inserted_id
    #             response = {
    #                 'insertion_id': str(insertion_id)
    #             }
    #             return response
    #     except Exception as e:
    #         raise e


    def check_if_at_least_one_restaurant(self, user_id):
        try:
            result = self.collection.find_one({
                    '_id': ObjectId(user_id)
                },{
                  'restaurants': 1
                }
            )
            if result is None: raise errors.UserNotPresentInDatabase()
            restaurants = result.get('restaurants', None)
            if len(restaurants) == 0: 
                return False
            else:
                return True
        except Exception as e:
            raise e


    # TO DO - Expand error handling capabilities on such functions, right now we're just returning if we get that far
    @decorators.print_func_name()
    def insert_restaurants(self, user_id, restaurants):
        try:
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
        except Exception as e:
            pass


    @decorators.print_func_name()
    def retrieve_page_of_restaurants(self, user_id, limit, offset):
        try:
            print('LIMIT', limit)
            print('OFFSET', offset)
            response = self.collection.find({
                '_id': ObjectId(user_id),
                },
                {
                    "restaurants": { 
                        "$slice": [ offset , limit ] 
                    }  
                }
            )
            # print(list(response))
            page = response[0]['restaurants']
            # print(page)
            return page
        except Exception as e:
            print('Error thrown', e)
            pass



class Locations(Database):
    def __init__(self):
        super().__init__()
        self.location_structure = {
            "location_name": None,
            "latitude": None,
            "longitude": None
        }


    @decorators.print_func_name()   
    def insert_new_location(self, user_id, body):
        # for now, just use default location structure
        # print(user_id, body)
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


    @decorators.print_func_name()   
    def update_location(self, user_id, location_id, body):
        try:
            print('body is', body)
            base_set_path = f"locations.{location_id}"
            set_object = {}
            for key in body.keys():
                set_object[f"{base_set_path}.{key}"] = body.get(key)
            print(set_object)
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
        except Exception as e:
            raise e


    @decorators.print_func_name()   
    def retrieve_all_locations(self, user_id):
        try:
            result = self.collection.find_one({
                    '_id': ObjectId(user_id)
                },{
                  'locations': 1
                }
            )
            if result is None: raise errors.UserNotPresentInDatabase()
            locations = result.get('locations', None)
            if locations is None: raise errors.NoLocationsForThisUser()
            return locations
        except Exception as e:
            raise e


    @decorators.print_func_name()   
    def check_if_at_least_one_location(self, user_id):
        try:
            result = self.collection.find_one({
                    '_id': ObjectId(user_id)
                },{
                  'locations': 1
                }
            )
            if result is None: raise errors.UserNotPresentInDatabase()
            print(result)
            locations = result.get('locations', None)
            print(locations)
            if locations is None or len(locations) == 0: raise errors.NoLocationsForThisUser()
            return locations
        except Exception as e:
            raise e


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