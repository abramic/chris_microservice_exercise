class BackendDefinedErrors(Exception):
     def __init__(self):   
        self.error_code = None
        self.message = None

class RestaurantGetRequestInsertion(BackendDefinedErrors):
    def __init__(self):
        super().__init__()
        self.error_code = 600
        self.message = 'There was an error inserting into the database'

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


class YelpConcurrencyError():
    pass