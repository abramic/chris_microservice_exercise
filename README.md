# chris_microservice_exercise

## ENDPOINT: /locations

### GET all locations

```
Required request parameters
  user_id
```

### PATCH location

```
Required request parameters
  user_id
  location_id
  
  If location_id is present in the query string, items passed back in the payload get overwritten (items not passed back will   remain unchanged).  

  Otherwise, location is added to user's locations object in the database

Payload:  

 {
   "location": "new_york",
   "latitude": 40.785091,
   "longitude": -73.968285
 }
 
 If location_id is not present in the query string, all props must be included
```
 
## ENDPOINT: /restaurants

```
Required request parameters
  user_id
```
### GET all businesses

#### Request parameters / payload

  ```
  Optional request parameters
    limit (defaults to 20 if nothing is specified)
    offset
  
  Payload: {}
  ```

#### Response Object:

  ```
  {
     businesses: [
        {
           name: "Central Park",
           id: "34er34kj3re3w4w34wk34w3qk4",
           review_count: 2388
           city: "New York"
        }
        ...up to 20 more businesses
     ]
     total_for_user: 983
  }
  ```

Note: If values not yet in database, this endpoint will pull for all locations entered for user
      If no locations have been entered, user will be prompted to add at least a single location prior to doing a data pull
