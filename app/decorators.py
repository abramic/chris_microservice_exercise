from functools import wraps
from flask import make_response, request
from json import dumps

import time
import errors
import helpers


def print_func_name():
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            print('Invoking ' + f.__name__)
            return f(*args, **kwargs)
        return decorated
    return decorator


def check_for_integer_params(params: list):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            try:
                for param in params:
                    value = request.args.get(param)
                    param_as_int = int(value)
                    if param_as_int != 0:
                        if float(value) / int(value) != 1.0: raise Exception()
                        if param_as_int < 0: raise Exception()
                        if param_as_int < 1 and param == 'limit': raise Exception()
                return f(*args, **kwargs)
            except Exception as e:
                print(e)
                error_response = helpers.format_error_message(errors.ParamMustBeInteger())
                return make_response(error_response, 400) 
        return decorated
    return decorator


def allowed_methods(allowed_methods):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if request.method not in allowed_methods:
                new_error = errors.EndpointMethodNotAllowed()
                error_message = helpers.format_error_message(new_error)
                return make_response(error_message, 405)
            return f(*args, **kwargs)
        return decorated
    return decorator


def check_for_user_name():
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if 'user_name' not in request.args.keys():
                error_response = helpers.format_error_message(errors.MissingUserNameInQueryString())
                return make_response(error_response, 400)
            else:
                return f(*args, **kwargs)
        return decorated
    return decorator


def check_for_user_id():
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if 'user_id' not in request.args.keys():
                error_response = helpers.format_error_message(errors.MissingUserIdInQueryString())
                return make_response(error_response, 400)
            else:
                return f(*args, **kwargs)
        return decorated
    return decorator


def handle_errors():
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            result = make_response('message: Unknown issue', 500)
            try:
                result = f(*args, **kwargs)                
            except Exception as e:
                parent_class = errors.BackendDefinedErrors()
                if isinstance(e, type(parent_class)):
                    message = helpers.format_error_message(e)
                    result = make_response(message, 400)                    
                else:
                    result = make_response({'message': f"{e}"}, 500)
            finally:
                return result
        return decorated
    return decorator


def retry_func(retries=10):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            try:
                result = f(*args, **kwargs)
                return result
            except Exception as e:
                if type(e).__name__ in ['YelpConcurrencyError']:
                    remaining = retries
                    while remaining >= 1:
                        time.sleep(1)
                        new_response = f(*args, **kwargs)
                        if new_response.get('status_code' != 200):
                            remaining -= 1
                            continue
                        else:
                            return new_response
                    return []
                else:
                    return []
        return decorated
    return decorator


def basic_validate_against_model_locations(model, all_props_required):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            body = request.get_json()
            body_type = type(body).__name__ 
            model_type = type(model).__name__
            if body_type != model_type: raise errors.RequestBodyPropTypeError('Request Body', body_type, model_type)

            return f(*args, **kwargs)
        return decorated
    return decorator


