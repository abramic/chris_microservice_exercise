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

# can we invoke this in such a way that we throw the errors into the handle_errors decorator, to ensure that all errors get handled in the same place?
# we could just do this validation in handle errors, I suppose but we may not want it/need it for every endpoint (and we'd want to call handle_errors on most all endpoints)
def check_for_user_id():
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            default_response = helpers.format_error_message(errors.BackendDefinedErrors())
            result = make_response(default_response, 500)
            try:
                if 'user_id' not in request.args.keys():
                    error_response = helpers.format_error_message(errors.MissingUserIdInQueryString())
                    result = make_response(error_response, 400)
                else:
                    result = f(*args, **kwargs)
            except Exception as e:
                    error_message = helpers.format_error_message(errors.DefaultBackendResponse(e))
                    result = make_response(error_response, 500)
            finally:
                return result
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
                    # print('Message ', message)
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




