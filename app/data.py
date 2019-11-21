from threading import Thread
from functools import reduce, wraps
from json import dumps

import decorators
import orm
import helpers
import errors


location_structure = {
    "location_name": 'str',
    "latitude": 'str',
    "longitude": 'str'
} 


@decorators.print_func_name()
def make_get_request_from_yelp_just_businesses(connection, parameters, businesses):
    response = connection.get(parameters)
    if 'businesses' in response:
        local_businesses = response.get('businesses')
        # why can't we return a new concatenated array using unpacking, here when done as part of a thread?
        # maybe append doesn't trigger a race condition, but unpacking could (or cause we're operating on a new list in memory if we concatenate)
        for item in local_businesses:
            businesses.append(item)
    return businesses


@decorators.print_func_name()
def make_requests_for_single_city(name, latitude, longitude, results):
    limit = 50
    offset = 0
    parameters = {
        'limit': 50,
        'offset': offset,
        'latitude': latitude,
        'longitude': longitude,
        'radius': 500
    }
    yelp = orm.Yelp()
    response = yelp.get(parameters)

    offset += limit
    total_businesses = [*response['businesses']]
    if offset < response['total']:
        while offset < response['total']:
            # Looping solution
            parameters.update({'offset': offset})
            total_businesses = make_get_request_from_yelp_just_businesses(yelp, parameters, total_businesses)
            offset += limit

            # Threading solution

            #
            # subthreads = []
            # # There's some kind of issue here which seems to relate to how parameters are passed into args for the Thread
            #     pag_parameters = {
            #         'limit': 50,
            #         'offset': offset,
            #         'latitude': latitude,
            #         'longitude': longitude,
            #         'radius': 500
            #     }
            #
            #     parameters.update({'offset': offset})
            #     # pag_parameters = parameters
            #     # print(pag_parameters)
            #     process = Thread(target=make_get_request_from_yelp_just_businesses, args=[pag_parameters, headers, total_businesses])
            #     subthreads.append(process)
            #     offset += limit
            #
            # for process in subthreads:
            #     process.start()
            # for process in subthreads:
            #     process.join()

            # response['businesses'] = total_businesses
    results = helpers.modify_businesses(total_businesses, results, name)
    return results


def retrieve_for_multiple_cities(user_id, locations):
    results = []
    threads = []
    for id, city in locations.items():
        process = Thread(target=make_requests_for_single_city,
                            args=[city.get('location'), city.get('latitude'), city.get('longitude'), results])
        threads.append(process)

    for process in threads:
        process.start()
    for process in threads:
        process.join()

    db = orm.Restaurants()
    response = db.insert_restaurants(user_id, results)
    return response


@decorators.print_func_name()
def add_new_user(user_name):
    db = orm.User(user_name)
    response = db.insert_new_user()
    return response


# TO DO - See if can refactor add_location, update_location and get_all_locations into a single function
@decorators.print_func_name()
@decorators.basic_validate_against_model_locations(location_structure, True)
def add_location(user_id, body):
    db = orm.Locations()
    response = db.insert_new_location(user_id, body)
    return response


@decorators.print_func_name()
def update_location(user_id, location_id, body):
    db = orm.Locations()
    response = db.update_location(user_id, location_id, body)
    return response


@decorators.print_func_name()
def get_all_locations(user_id):
    db = orm.Locations()
    response = db.retrieve_all_locations(user_id)
    return response


@decorators.print_func_name()
def check_if_at_least_one_location(user_id):
    db = orm.Locations()
    response = db.check_if_at_least_one_location(user_id)
    return response


@decorators.print_func_name()
def check_if_at_least_one_restaurant(user_id):
    db = orm.Restaurants()
    response = db.check_if_at_least_one_restaurant(user_id)
    return response


@decorators.print_func_name()
def retrieve_page_of_restaurants(user_id, limit, offset):
    db = orm.Restaurants()
    page = db.retrieve_page_of_restaurants(user_id, limit, offset)
    return page

# should take two inputs: the request data structure and the required data structure
# will compare the prop name and also the type in both recursively and let the user know if a prop is in there that shouldn't be and if there are type mismatches

