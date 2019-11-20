from flask import Flask, request, make_response, jsonify
from dotenv import load_dotenv

import decorators
import data
import orm

load_dotenv()
app = Flask("chris_server")


@decorators.print_func_name()
@app.route('/')
def hello():
    return "Hello World!"


@app.route('/restaurants', methods = ['GET', 'PATCH', 'POST', 'PUT', 'DELETE'])
@decorators.print_func_name()
@decorators.allowed_methods(['GET'])
@decorators.check_for_user_id()
@decorators.check_for_integer_params(['limit', 'offset'])
@decorators.handle_errors()
def handle_yelp_data():
    user_id = request.args.get('user_id')
    limit = int(request.args.get('limit', 20))
    offset = int(request.args.get('offset', 0))
    locations = data.check_if_at_least_one_location(user_id)
    restaurants_present = data.check_if_at_least_one_restaurant(user_id)
    if restaurants_present is False:
        data.retrieve_for_multiple_cities(user_id, locations)
    restaurants_page = data.retrieve_page_of_restaurants(user_id, limit, offset)
    return make_response(jsonify(restaurants_page), 200)


@app.route('/locations', methods = ['GET', 'PATCH', 'POST', 'PUT', 'DELETE'])
@decorators.print_func_name()
@decorators.allowed_methods(['GET', 'PATCH'])
@decorators.check_for_user_id()
@decorators.handle_errors()
def handle_locations():
    user_id = request.args.get('user_id')
    if(request.method == 'PATCH'):
        body = request.get_json()
        if(request.args.get('location_id') == None):
            response = data.add_location(user_id, body)
            return make_response(response, 201)
        else:
            location_id = request.args.get('location_id')
            response = data.update_location(user_id, location_id, body)
            return make_response(response, 204)
    elif(request.method == 'GET'):
        response = data.get_all_locations(user_id)
        return make_response(response, 200)


@app.route('/users', methods = ['GET', 'PATCH', 'POST', 'PUT', 'DELETE'])
@decorators.print_func_name()
@decorators.allowed_methods(['POST'])
@decorators.check_for_user_name()
@decorators.handle_errors()
def add_user():
    user_name = request.args.get('user_name')
    response = data.add_new_user(user_name)
    print(response)
    return make_response(response, 200)


app.run(port=int('5001'), debug=True)
# app.run(host='0.0.0.0', port=int('5001'), debug=True)

# app.run(debug=True)


# content for test commit
















