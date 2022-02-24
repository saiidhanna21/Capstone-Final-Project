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
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`,  
- Authentication: Auth0 

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
- 404: Resource Not Found
- 405: Method Not Allowed 

### Endpoints
#### GET /actors
- General:
    - Return a list of actors
- Sample: `curl http://127.0.0.1:5000/actors`

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

### GET /questions/{page_id}
- General:
    - Returns a list of questions objects, totalQuestions, categories and current category
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
`curl http://127.0.0.1:5000/questions/1` 

```
{
  "categories": [
    {
      "id": 1,
      "type": "Science"     
    },
    {
      "id": 2,
      "type": "Art"
    },
    {
      "id": 3,
      "type": "Geography"   
    },
    {
      "id": 4,
      "type": "History"     
    },
    {
      "id": 5,
      "type": "Entertainment"
    },
    {
      "id": 6,
      "type": "Sports"      
    }
  ],
  "currentCategory": "Science",
  "question": [
    {
      "answer": "Muhammad Ali",
      "category": 4,        
      "difficulty": 1,      
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,        
      "difficulty": 4,      
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,        
      "difficulty": 3,      
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Brazil",   
      "category": 6,        
      "difficulty": 3,      
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",  
      "category": 6,        
      "difficulty": 4,      
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"      
    },
    {
      "answer": "George Washington Carver",
      "category": 4,        
      "difficulty": 2,      
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,        
      "difficulty": 2,      
      "id": 13,
      "question": "What is the largest lake in Africa?" 
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,        
      "difficulty": 3,      
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors"       
    },
    {
      "answer": "Agra",     
      "category": 3,        
      "difficulty": 2,      
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,        
      "difficulty": 2,      
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ],
  "totalQuestions": 28      
}
```
    
### GET /categories/{question_id}/questions
- General:
    - Returns a list of questions objects that have same category, totalQuestions, and current category
`curl http://127.0.0.1:5000/categories/1/questions`

``` {
  "currentCategory": "Science",
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,        
      "difficulty": 4,      
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,        
      "difficulty": 3,      
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",    
      "category": 1,        
      "difficulty": 4,      
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?" 
    }
  ],
  "totalQuestions": 28      
}
```
### POST /quizzes
- General:
  - Check the category choosed and not in previous questions. Returns success and questions related to that category
` curl -X POST -H "Content-Type: application/json" -d '{"previous_questions":[19],"category":1}' http://127.0.0.1:5000/quizzes`
```
{
  "question": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"       
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "fine",
      "category": 1,
      "difficulty": 1,
      "id": 38,
      "question": "How are you"
    },
    {
      "answer": null,
      "category": 1,
      "difficulty": null,
      "id": 39,
      "question": null
    }
  ],
  "success": true
}
```


### POST /questions
- General:
  - Creates a new question using the submitted question, answer, difficulty and category. Returns success value.
`  curl -X POST -H "Content-Type: application/json" -d '{"question":"How are you", "answer":"fine", "difficulty":1,"category":1}' http://127.0.0.1:5000/questions `
```
{
  "success": true
}
```

### DELETE /questions/{question_id}
- General:
  - delete a question by its id. Return a succes value and the id of the question deleted
`curl -X DELETE http://127.0.0.1:5000/questions/29 `
``` 
  {
  "deleted_id": 29,
  "success": true
}
```
## Deplpyment N/A

## Authors

Saiid Hanna

## Acknowledgments
Hope it can facilate a lot of hard works