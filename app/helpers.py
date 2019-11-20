# Eventually, add some validation in here against our db object model for restaurant
def modify_businesses(businesses_for_city, businesses_for_all_cities, city_name):
    for  business in businesses_for_city:
        businesses_for_all_cities.append({
            'name': business.get('name', None),
            'yelp_id': business.get('id', None),
            'review_count': business.get('review_count', None),
            'city': city_name
        })
    return businesses_for_all_cities
        

def format_error_message(error):
    return {
        'error_code': error.error_code,
        'message': error.message
    }


def validate_location_name(body):
    pass
