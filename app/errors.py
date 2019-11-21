class BackendDefinedErrors(Exception):
     def __init__(self):   
        self.error_code = None
        self.message = 'Default Backend Response'


class DefaultBackendResponse(BackendDefinedErrors):
    def __init__(self, e):
        super().__init__()
        self.error_code = 500
        self.message = e   


# HTTP Errors


class EndpointMethodNotAllowed(Exception):
    def __init__(self):
        super().__init__()
        self.error_code = 405
        self.message = 'Method not allowed for this endpoint'


# Database Errors


class RestaurantGetRequestInsertion(BackendDefinedErrors):
    def __init__(self):
        super().__init__()
        self.error_code = 601
        self.message = 'There was an error inserting into the database'


class DatabaseUserInsertion(BackendDefinedErrors):
    def __init__(self):
        super().__init__()
        self.error_code = 602
        self.message = 'There was an error the user information into the database'


class DatabaseLocationInsertion(BackendDefinedErrors):
    def __init__(self, message):
        super().__init__()
        self.error_code = 603
        self.message = message


class RestaurantDataForUserNotFound(BackendDefinedErrors):
    def __init__(self):
        super().__init__()
        self.error_code = 604
        self.message = 'Restaurant data for the user was not found in the database' 


class UserNotPresentInDatabase(BackendDefinedErrors):
    def __init__(self):
        super().__init__()
        self.error_code = 605
        self.message = 'User id is not present in database'


class NoLocationsForThisUser(BackendDefinedErrors):
    def __init__(self):
        super().__init__()
        self.error_code = 606
        self.message = 'No locations for this user' 


# Validation Errors (In query string)


class MissingUserIdInQueryString(BackendDefinedErrors):
    def __init__(self):
        super().__init__()
        self.error_code = 701
        self.message = 'Please provide a user id' 


class MissingUserNameInQueryString(BackendDefinedErrors):
    def __init__(self):
        super().__init__()
        self.error_code = 702
        self.message = 'Please provide a user name' 


class ParamMustBeInteger(BackendDefinedErrors):
    def __init__(self):
        super().__init__()
        self.error_code = 703
        self.message = 'Limit and offset must be integers.  Limit must be greater than zero, and offset can be greater than or equal to zero'    


class LimitTooLarge(BackendDefinedErrors):
    def __init__(self, limit):
        super().__init__()
        self.error_code = 704
        self.message = f'Limit of {limit} to large.  Must be a positive integer less than or equal to 20' 


# Validation Errors (In payload)


class RequestBodyPropValidationError(BackendDefinedErrors):
    def __init__(self, prop):
        super().__init__()
        self.error_code = 801
        self.message = f'Request body data structure should not contain the following property: {prop}'    


class RequestBodyPropTypeError(BackendDefinedErrors):
    def __init__(self, prop, user_type, appropriate_type):
        super().__init__()
        self.error_code = 802
        self.message = f'Error on the following request prop: {prop}.  Type {user_type} is not correct.  Use {appropriate_type} instead'  


class RequiredPropNotPresent(BackendDefinedErrors):
    def __init__(self, prop):
        super().__init__()
        self.error_code = 803
        self.message = f'Required Prop: {prop} not present.'  


class ExtraPropsInRequestBody(BackendDefinedErrors):
    def __init__(self, prop):
        super().__init__()
        self.error_code = 803
        self.message = f'Extra Prop {prop} present in request body.'  


class YelpConcurrencyError():
    pass