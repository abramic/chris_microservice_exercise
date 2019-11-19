# Eventually, add some validation in here against our db object model for restaurant
def modify_businesses(businesses_for_city, businesses_for_all_cities, city_name):
    try:
        for  business in businesses_for_city:
            businesses_for_all_cities.append({
                'name': business.get('name', None),
                'yelp_id': business.get('id', None),
                'review_count': business.get('review_count', None),
                'city': city_name
            })
        return businesses_for_all_cities
        

    except Exception as e:
        print('Error is', e)
        raise e




def format_error_message(error):
    try:
        print(error.error_code)
        print(error.message)
        return {
            'error_code': error.error_code,
            'message': error.message
        }
    except Exception as e:
        print(e)
        return {
            'error_code': 500,
            'message': 'Format error message'
        }
