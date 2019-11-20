from flask import Flask, request, make_response, jsonify
from dotenv import load_dotenv

import decorators
import data
import orm

load_dotenv()
app = Flask("chris_server")


@app.route('/')
def hello():
    return "Hello World from new repo file!"


@app.route('/retrieveForMultipleCities')
@decorators.print_func_name()
@decorators.check_for_user_id()
@decorators.handle_errors()
def handle_yelp_data():
    try:
        user_id = request.args.get('user_id')
        locations = data.check_if_at_least_one_location(user_id)
        restaurants_present = data.check_if_at_least_one_restaurant(user_id)
        if restaurants_present is False:
            data.retrieve_for_multiple_cities(user_id, locations)
            return make_response('Restaurants Added From Yelp!', 200)
        else:
            return make_response('Restaurants Already There!', 200)
    except Exception as e:
        # print(e)
        raise e


@app.route('/locations', methods = ['GET', 'PATCH'])
@decorators.print_func_name()
@decorators.check_for_user_id()
@decorators.handle_errors()
def handle_locations():
    try:
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
        else:
            raise Exception()
    except Exception as e:
        print(e)
        raise e


@app.route('/users', methods = ['POST'])
@decorators.print_func_name()
# @decorators.check_for_user_id()
@decorators.handle_errors()
def add_user():
    try:
        user_name = request.args.get('user_name')
        response = data.add_new_user(user_name)
        print(response)
        return make_response(response, 200)

    except Exception as e:
        print(e)
        raise e

app.run(port=int('5001'), debug=True)
# app.run(host='0.0.0.0', port=int('5001'), debug=True)

# app.run(debug=True)















