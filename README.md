# Backend - Full Stack CapstonProject
This project is designed for a Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies.

### Installing Dependencies for the Backend

1. **Python 3.9** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
source setup.sh
source auth_setup.sh  #To be able to use the jwt token for specific permissions
python app.py
```

The `setup.sh` contanins 2 databases one for testing and the other for the actual site.

## Testing
To run the tests, run
```
python test_flaskr.py
```

## API Reference

### Getting Started
- Base URL: At present this app can be run locally and is hosted using heroku. The backend app is hosted at, `https://myfirstapp210.herokuapp.com/`,  
- Authentication: Bearer token 

### Authentication 
- Using Auth0 and jwt tokens for authorization (Bearer token)
- Roles:
    - Casting Assistant
          Can view actors and movies
    - Casting Director
          All permissions a Casting Assistant has and…
          Add or delete an actor from the database
          Modify actors or movies
    - Executive Producer
          All permissions a Casting Director has and…
          Add or delete a movie from the database
### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 401: Lacks valid authentication
- 404: Resource Not Found
- 405: Method Not Allowed 

### Endpoints
#### GET /actors
- General:
    - Return a list of actors
- Who can make this request:
  Users with these roles
    - Casting Assistant
    - Casting Director
    - Executive Producer
- Sample: `curl -H "Authorization: Bearer ${assistant_token}" https://myfirstapp210.herokuapp.com/actors`

``` {
    "actors": [
        {
            "age": 19,
            "career": "action",
            "experience": 0,
            "id": 1,
            "name": "saiid",
            "projects": "x"
        },
        {
            "age": 20,
            "career": "drama",
            "experience": 3,
            "id": 2,
            "name": "roy",
            "projects": "y"
        },
        {
            "age": 20,
            "career": "drama",
            "experience": 0,
            "id": 13,
            "name": "paul",
            "projects": "z"
        },
        {
            "age": 20,
            "career": "drama",
            "experience": 0,
            "id": 14,
            "name": "stephan",
            "projects": "o"
        }
    ]
}
```
### GET /movies
- General : 
    - return a list of movies
- Who can make this request:
  Users with these roles
    - Casting Assistant
    - Casting Director
    - Executive Producer
### GET /plays
- General :
    - return a list of plays
- Who can make this request:
  Users with these roles
    - Casting Assistant
    - Casting Director
    - Executive Producer

### GET /movies/{movies_id}
- General:
    - Returns a detailed information about the movie with id 1
- Who can make this request:
  Users with these roles
    - Casting Assistant
    - Casting Director
    - Executive Producer
- Sample: `curl -H "Authorization: Bearer ${assistant_token}" https://myfirstapp210.herokuapp.com/movies/1` 
- Note: `Token` is equal to the token mentioned in the test_app.py
```
{
    "estimated_project_time": 60,
    "id": 1,
    "name": "fast",
    "need_actors": true
}
```
### GET /actors/{actors_id}
- General :
    - Return a detailed information about the actor with id actors_id
- Who can make this request:
  Users with these roles
    - Casting Assistant
    - Casting Director
    - Executive Producer   
### POST /actors
- General:
  - Add an actor 
- Who can make this request:
  Users with these roles
    - Casting Director
    - Executive Producer
- Sample: `curl -X POST -H "Authorization: Bearer ${director_token}" -H "Content-Type: application/json" -d '{"name":"chriss","age":20,"career":"drama","projects":"c","experience":0}' https://myfirstapp210.herokuapp.com/actors`
```
{
  "actor_added": {
    "age": 20,
    "career": "drama",
    "experience": 0,
    "id": 19,
    "name": "chriss",
    "projects": "c"
  }
}
```
### POST /movies
- General:
  - Creates a new movie
- Who can make this request:
  Users with these roles
    - Executive Producer
- Sample: `curl -X POST -H "Authorization: Bearer ${producer_token}" -H "Content-Type: application/json" -d '{"name":"original","estimated_project_time":70,"need_actors":true}' https://myfirstapp210.herokuapp.com/movies`

{
  "movie_added": {
    "estimated_project_time": 70,
    "id": 9,
    "name": "original",
    "need_actors": true
  }
}
### POST /plays
- General 
  - Creates a new play using an existing id in movies and actors
- Who can make this request:
  Users with these roles
    - Executive Producer
### DELETE /actors/{actors-id}
- General:
  - delete an actor by its id. Return the id of the actor deleted
- Who can make this request:
  Users with these roles
    - Casting Director
    - Executive Producer
- Sample: `curl -X DELETE -H "Authorization: Bearer ${director_token}" https://myfirstapp210.herokuapp.com/actors/2`
``` 
  {
  "deleted_id": 2,
}
```
### DELETE /movies/{movies-id}
- General:
  - delete a movie by its id. Return the id of the movie deleted
- Who can make this request:
  Users with these roles
    - Executive Producer

### DELETE /plays/{plays-id}
- General:
  - delete a play by its id. Return the id of the play deleted
- Who can make this request:
  Users with these roles
    - Executive Producer

### PATCH /movies/{movies-id}
- General:
  - edit the informations of a movie
- Who can make this request:
  Users with these roles
    - Casting Director
    - Executive Producer
- Sample: `curl -X PATCH -H "Authorization: Bearer ${director_token}" -H "Content-Type: application/json" -d '{"name":"originals","estimated_project_time":50,"need_actors":false}' https://myfirstapp210.herokuapp.com/movies/1`
```
{
  "updated_movie": {
    "estimated_project_time": 60,
    "id": 1,
    "name": "originals",
    "need_actors": false
  }
}
```
### PATCH /actors/{actors-id}
- General:
  - edit the informations of an actor
- Who can make this request:
  Users with these roles
    - Casting Director
    - Executive Producer
### PATCH /plays/{plays-id}
- General:
  - edit the informations of a play
- Who can make this request:
  Users with these roles
    - Executive Producer

## Deplpyment N/A

## Authors

Saiid Hanna

## Acknowledgments
Hope it can facilate a lot of hard works