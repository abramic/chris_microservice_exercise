# chris_microservice_exercise

## ENDPOINT: /locations

### GET

#### Request
```
Required request parameters
  user_id
```
#### Response
```
Status Code: 200
Response Body: 

[
   {
     "id": "awelkrerk3434k3q43ak4343a4kq",
     "location": "New York",
     "latitude": 40.785091,
     "longitude": -73.968285
   }
  ...as many locations as exist for that user
]
```


### PATCH

#### Request
```
Required request parameters
  user_id
  location_id
  
  If location_id is present in the query string, items passed back in the payload get overwritten (items not passed back will   remain unchanged).  

  Otherwise, location is added to user's 'locations' information in the database

Payload:  

 {
   "location": "new_york",
   "latitude": 40.785091,
   "longitude": -73.968285
 }
 
 If location_id is not present in the query string, all props must be included
```
#### Response

```
Status Code: 201 (if newly created) 204 (if updated)
Response Body:

{
  "id": "2k323kekf3k3q43k3qk3etk43q43k"
}

```
 
## ENDPOINT: /restaurants

```
Required request parameters
  user_id
```
### GET

#### Request

  ```
  Optional request parameters
    limit (defaults to 20 if nothing is specified)
    offset
  
  Payload: {}
  ```

#### Response:

  ```
  Status Code: 200
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

Note: If values not yet in database, this endpoint will pull for all locations entered for user.  If no locations have been entered, user will be prompted to add at least a single location prior to doing a data pull
