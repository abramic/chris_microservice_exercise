from threading import Thread
from functools import reduce, wraps
from json import dumps

import decorators
import orm
import helpers
# import errors


def create_dictionary_of_restaurant_names(city):
    businesses = city.get('businesses')

    if businesses is not None:
        city['chris_keys_check'] = len(city['businesses'])
        def reducer(acc, item):
            if item.get('alias') is not None:
                name = item.get('alias')
                if acc.get(name) is not None:
                    acc[name] += 1
                else:
                    acc[name] = 1
            return acc
        city['businesses'] = reduce(reducer, businesses, {})
    else:
        city['businesses'] = {
            'error': 'Error in reduce'
        }
    return city


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
    try:
        # first page
        limit = 50
        offset = 0
        # do the first one on its own
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
        # Create dictionary of names for each
    except Exception as e:
        raise e


def retrieve_for_multiple_cities(request):
    results = []
    cities = request.get_json()

    try:
        user_id = request.args.get('user_id')
        threads = []
        # raise errors.RestaurantGetRequestInsertion()
        # raise errors.ChrisError()
        for city in cities:
            process = Thread(target=make_requests_for_single_city,
                             args=[city.get('location'), city.get('latitude'), city.get('longitude'), results])
            threads.append(process)

        for process in threads:
            process.start()
        for process in threads:
            process.join()
# Additional code to practice pythons native reduce function
        # for city, vals in results.items():
        #     results[city] = create_dictionary_of_restaurant_names(vals)
        results = {
            'user_id': user_id,
            'results': results,
        }

        db = orm.Restaurants()
        print(type(results))
        response = db.insert_new_restaurants_for_user(results)
        return response

    except Exception as e:
        print(e)
        raise e