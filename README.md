# Casting Agency FSND Capstone Project

The Casting Agency API is responsible for creating and managing movies and actors. There are Three different user roles: Casting Assistant, Casting Director and Executive Producer.

### Roles:

Casting Assistant: Related permissions are view actors and movies.
Casting Director: Related permissions are view, add, modify, or delete actors.
Executive Producer: Related permissions are view, add, modify, or delete actors and movies.

# Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Running the server

To run the server, execute:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```
Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

## API Documentation

# GET Endpoints

GET '/movies'
- Retrieves all movies.
- Request Arguments: None
- Returns: all movies with its corresponding ids and total number of movies.

```
Example:
{
    "movies": [
        {
            "id": 9,
            "release_date": "Tue, 08 Sep 2020 00:00:00 GMT",
            "title": "Alive"
        },
        {
            "id": 10,
            "release_date": "Wed, 02 Oct 2019 00:00:00 GMT",
            "title": "Joker"
        }
    ],
    "success": true,
    "total": 2
}

```
GET '/actors'
- Retrieves all actors.
- Request Arguments: None.
- Returns:all actors with its corresponding ids and total number of actors.

```
Example:

    "actors": [
        {
            "age": "44",
            "gender": "Male",
            "id": 10,
            "name": "Jim"
        },
        {
            "age": "23",
            "gender": "female",
            "id": 11,
            "name": "Noor"
        }
    ],
    "success": true,
    "total": 2
}

```
GET '/movies/<int:id>'
- Retrieves a movie corresponding to requested id.
- Request Arguments: movie id.
- Returns: Current movie related id.
 
```
Example:
{
movies:{"id":10,"release_date":"Wed, 02 Oct 2019 00:00:00 GMT","title":"Joker"},"success":true}
}

```
GET '/actors/<int:id>'
- Retrieves an actor corresponding to requested id.
- Request Arguments: movie id.
- Returns: Current movie related id.
 
```
Example:
{
"actor":{"age":"44","gender":"Male","id":10,"name":"Jim"},"success":true 
}

```
# POST Endpoints

POST '/movies'
- Add a new movie.
- Request body: title and release date.
- Returns: 
        - Created movie information.

```
Example:
{
    "movie": {
        "id": 10,
        "release_date": "Wed, 02 Oct 2019 00:00:00 GMT",
        "title": "Joker"
    },
    "success": true
}
```
POST '/actors'
- Add a new actor.
- Request body: name, age and gender.
- Returns: 
        - Created actor information.

```
Example:
{
    "actor": {
        "age": "44",
        "gender": "Male",
        "id": 10,
        "name": "Jim"
    },
    "success": true
}
```
# PATCH Endpoint

PATCH '/movies/<int:id>'
- updates an existing movie in the database.
- Request arguments: movie id.
- Returns: 
        - Updated movie information.

```
Example: curl -X PATCH -H "Authorization: Bearer access_token" -H "Content-Type: application/json" -d '{"release_date": "9 oct 2020"}' http://127.0.0.1:5000/movies/9
{
    "movies": {
        "id": 9,
        "release_date": "Fri, 09 Oct 2020 00:00:00 GMT",
        "title": "Alive"
    },
    "success": true
}
```
PATCH '/actors/<int:id>'
- updates an existing actor in the database.
- Request arguments: actor id.
- Returns: 
        - Updated actor information.

```
Example: curl -X PATCH -H "Authorization: Bearer access_token" -H "Content-Type: application/json" -d '{"age": "34"}' http://127.0.0.1:5000/actors/10
{
{
    "actors": {
        "age": "34",
        "gender": "Male",
        "id": 10,
        "name": "Jim"
    },
    "success": true
}
}
```

# DELETE Endpoint

DELETE '/movies/<int:id>'
- Delete a movie with specified id.
- Request Arguments: movie id.
- Returns:
        - Deleted movie id.

```
Example:
{
    "deleted Movie id": 5,
    "success": true
}
```
DELETE '/actors/<int:id>'
- Delete an actor with specified id.
- Request Arguments: actor id.
- Returns:
        - Deleted actor id.

```
Example:
{
    "deleted actor id": 6,
    "success": true
}
```
# Error Handling
401 error
This error occurs when there is an issue with the authentication.

```
Example: 
{
    "error": 401,
    "message": "Authorization header is expected.",
    "success": false
}
403 error
This error occurs when user request not include required permission.

```
Example: 
{
    "error": 403,
    "message": "Permission not found.",
    "success": false
}

```
404 error 
This error occurs when server not able to locate resources or requested arguments.

```
Example: 
{
  "error": 404, 
  "message": "Resource Not Found", 
  "success": false
}

```
422 error 
This error occurs when server not able to process request body.

```
Example: 
{
  "error": 422,
  "message": "Unprocessable Entity",
  "success": false
}

```

## Testing
To run the tests, run
```
createdb agency_test

python test_app.py
```