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

        # Check if the item exists in the db
        # should always exist cause we validate for it in decorator
        user_id = request.args.get('user_id')
        db = orm.Restaurants()
        response = db.find_one(user_id)
        if response is not None:
            return make_response(jsonify({ 'message': 'values pulled earlier from Yelp.  Database not updated' }), 200)
        else:
            results = data.retrieve_for_multiple_cities(request)
            insertion_id = results.get('insertion_id')
            return make_response(jsonify({ 'message': f"values have been pulled from yelp and the insertion id is {insertion_id}" }), 200)

        return results
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
            # body = request.get_json()
            body = {}
            response = data.add_location(user_id, body)
            print(response)
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















