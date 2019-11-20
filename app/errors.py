class BackendDefinedErrors(Exception):
     def __init__(self):   
        self.error_code = None
        self.message = 'Default Backend Response'


class EndpointMethodNotAllowed(Exception):
    def __init__(self):
        super().__init__()
        self.error_code = 405
        self.message = 'Method not allowed for this endpoint'


class RestaurantGetRequestInsertion(BackendDefinedErrors):
    def __init__(self):
        super().__init__()
        self.error_code = 600
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
        self.error_code = 601
        self.message = 'Restaurant data for the user was not found in the database' 

class MissingUserIdInQueryString(BackendDefinedErrors):
    def __init__(self):
        super().__init__()
        self.error_code = 700
        self.message = 'Please provide a user id' 

class MissingUserNameInQueryString(BackendDefinedErrors):
    def __init__(self):
        super().__init__()
        self.error_code = 701
        self.message = 'Please provide a user name' 

class UserNotPresentInDatabase(BackendDefinedErrors):
    def __init__(self):
        super().__init__()
        self.error_code = 800
        self.message = 'User id is not present in database'

class NoLocationsForThisUser(BackendDefinedErrors):
    def __init__(self):
        super().__init__()
        self.error_code = 604
        self.message = 'No locations for this user'  

class DefaultBackendResponse(BackendDefinedErrors):
    def __init__(self, e):
        super().__init__()
        self.error_code = 500
        self.message = e   

class YelpConcurrencyError():
    pass