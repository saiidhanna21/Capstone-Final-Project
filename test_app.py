import os
from sre_constants import SUCCESS
import unittest
import json
from wsgiref import headers
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import delete
from auth import requires_auth
from app import create_app
from models import setup_db, Actor, Movie, Play


assistant_token='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InhIYm42LWNSSEtSX0ZjekkwLWp6ZiJ9.eyJpc3MiOiJodHRwczovL2Rldi1mODFpbXlyZC51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDEzNjE4OTE1ODEzNDU1NjQxODIiLCJhdWQiOiJDYXBzdG9uZSIsImlhdCI6MTY0NTcxNTc3NiwiZXhwIjoxNjQ1ODAyMTc2LCJhenAiOiJud1gySVlDYlU0a2lhM1BRNEFsb0JIZUgyV1IzQmREOSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJnZXQ6cGxheXMiXX0.maA6ih9gtJGt89UvtNieeTzoT_VsFQaR3tqnEkvYNmDBRtgIHEYDTziGGqzSJCmN7xpOTUDfBnsDOnVG0QhrleTP7vkHV15dh0AlIg8FFp0f_Q33T7InZmqcJbPGdS2qNFPskrVaGCk-eoyMb3jC6hyJIxczbCCBoj8_dyaGZyfRBuxir4qv_7485_2HZnQhybgSLnGynYhZ-wRBhBFkVbWRDWKQza2FTuh4SYEcC8vE_u0PLAzxJpQ-4sDqXlY4FgD6Fwy5k9XdA331iZ0-tA8buwgY3air-tNq4xZidaJaeoW7tpsGKY9dM4WYUQxzgtulFuFOTBCqWlGl7dCI8w'
director_token='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InhIYm42LWNSSEtSX0ZjekkwLWp6ZiJ9.eyJpc3MiOiJodHRwczovL2Rldi1mODFpbXlyZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjFmZmNlNDE0M2ZiNjcwMDY5YmFmYTg5IiwiYXVkIjoiQ2Fwc3RvbmUiLCJpYXQiOjE2NDU3MjkxMTcsImV4cCI6MTY0NTgxNTUxNywiYXpwIjoibndYMklZQ2JVNGtpYTNQUTRBbG9CSGVIMldSM0JkRDkiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsImdldDpwbGF5cyIsInBhdGNoOmFjdG9ycyIsInBvc3Q6YWN0b3JzIl19.lhBCEnQXb2_OOmuQ-kJUOQT4zQJ9BfDSxfiTMJVd9KVEgkmV0hVwj1QL0m6t75FeYhiKqzmRvLKSCuzOf84jNFzeC1xFVu4mRMnJeOTenwuHkE8qlShNjA2cOpGmjb8hxPX8SESfvVPf_fIRW1q9kXrFf4xpzkDXTE6sLkk5FUv55DYE6VefkF2wdbS1ZmRLAf-xHTySyS36wcCxpBTvUXb9gHcSD8GQZ6iQqY4DogyY4IZxMbtNB7-9ElhHtvuo6vaRZTAPIZj2h6eQ6Fyp-ReGQ660KmD6ZqUiwc9j0WdDhgHjQRbW3vxOVVQX5fWyqZDB5xu45_koppD7QNjLnA'
producer_token='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InhIYm42LWNSSEtSX0ZjekkwLWp6ZiJ9.eyJpc3MiOiJodHRwczovL2Rldi1mODFpbXlyZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjIxNzkxNjBjMjQyNzIwMDcwNjE5NTMxIiwiYXVkIjoiQ2Fwc3RvbmUiLCJpYXQiOjE2NDU3MjkyMTcsImV4cCI6MTY0NTgxNTYxNywiYXpwIjoibndYMklZQ2JVNGtpYTNQUTRBbG9CSGVIMldSM0JkRDkiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZGVsZXRlOnBsYXlzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJnZXQ6cGxheXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwYXRjaDpwbGF5cyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiLCJwb3N0OnBsYXlzIl19.XlqNuJXuDzAddCvOnDk4qy7L1e9Txglefj1EIfwU366t2BMlswHmBsIQcIXVqlA3WRqMgr37fnlmSp6mD9SJURy6HxwIowYj1_lkUEIA612RRvwNkKKWO8ypZrGlV-VyRF7Xf28wFqrpe4apYODOxNCDzV7rYEQzyfho-x-_QyPvus5Qcrz6H1mfMFvbEx9GbGCnxiBmXRpXPLigB_4MUZGhqB5RzXg7QJUGfO5bela6FHkEO7f5x4_R55ZY8uLMw7p_TtV5_jNY8azTKowx-LzeG97_dFG3yOnqW4nSjKLbaouH-F71-vb9q2ZOT_9sVsLjaqL9yOrE6FU3P9RpfQ'

assistant_header={
    'Authorization':'Bearer {}'.format(assistant_token)
} 

director_header={
    'Authorization':'Bearer {}'.format(director_token)
}   

producer_header={
        'Authorization':'Bearer {}'.format(producer_token)
    }

class CapstonProjectTestCase(unittest.TestCase):
    """This class represents the Capston Project test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_agency_test"
        self.database_path = "postgresql://postgres:1@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass
    
    def test_Actors(self):
        
        res = self.client().get('/actors',headers=assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data['actors'])
    
    def test_Actors_id(self):
        res = self.client().get('/actors/10',headers=assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data['name'])
        self.assertTrue(data['age'])
        self.assertTrue(data['career'])
        
    def test_Actors_id_error(self):
        res = self.client().get('/actors/100',headers=assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'])
        self.assertEqual(data['success'],False)
    
    def test_add_Actors(self):
        res = self.client().post('/actors',headers=director_header,json={"name":"joe","age":20,"career":"drama","projects":"","experience":0})
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['actor_added'])
    
    def test_add_Actors_method_error(self):
        res = self.client().delete('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,405)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'])
        self.assertEqual(data['success'],False)
    
    def test_add_Actors_request_error(self):
        res = self.client().post('/actors',headers=director_header,json={'name':'saiid'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,400)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'])
        self.assertEqual(data['success'],False)
    
    def test_delete_Actor(self):
        res = self.client().delete('/actors/3',headers=director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data['deleted_id'])
    
    def test_delete_Actors_method_error(self):
        res = self.client().post('/actors/1',headers=director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,405)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'])
        self.assertEqual(data['success'],False)
    
    def test_delete_Actors_request_error(self):
        res = self.client().delete('/actors/50',headers=director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'])
        self.assertEqual(data['success'],False)
    
    def test_edit_Actors(self):
        res = self.client().patch('/actors/1',headers=director_header,json={"name":"joe","age":20,"career":"drama","projects":"","experience":5})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data['updated_actor'])
    
    def test_edit_Actors_method_error(self):
        res = self.client().post('/actors/1',headers=director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,405)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'])
        self.assertEqual(data['success'],False)
    
    def test_edit_Actors_request_error(self):
        res = self.client().patch('/actors/100',headers=director_header,json={"name":"joe","age":20,"career":"drama","projects":"","experience":5})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'])
        self.assertEqual(data['success'],False)
    
    def test_Movies(self):
        res = self.client().get('/movies',headers=assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data['movies'])
    
    def test_Movies_id(self):
        res = self.client().get('/movies/1',headers=assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data['name'])
        self.assertTrue(data['estimated_project_time'])
        self.assertTrue(data['need_actors'])
        
    def test_Movies_id_error(self):
        res = self.client().get('/movies/100',headers=assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'])
        self.assertEqual(data['success'],False)
    
    def test_add_Movies(self):
        res = self.client().post('/movies',headers=producer_header,json={"name":"original","estimated_project_time":70,"need_actors":True})
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['movie_added'])
    
    def test_add_Moives_method_error(self):
        res = self.client().delete('/movies',headers=producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,405)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'])
        self.assertEqual(data['success'],False)
    
    def test_add_Movies_request_error(self):
        res = self.client().post('/movies',headers=producer_header,json={'name':'saiid'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,400)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'])
        self.assertEqual(data['success'],False)
    
    def test_delete_Movie(self):
        res = self.client().delete('/movies/2',headers=producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data['deleted_id'])
    
    def test_delete_Movies_method_error(self):
        res = self.client().post('/movies/1',headers=producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,405)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'])
        self.assertEqual(data['success'],False)
    
    def test_delete_Movies_request_error(self):
        res = self.client().delete('/movies/50',headers=producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'])
        self.assertEqual(data['success'],False)
    
    def test_edit_Movies(self):
        res = self.client().patch('/movies/1',headers=producer_header,json={"name":"original","estimated_project_time":70,"need_actors":True})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data['updated_movie'])
    
    def test_edit_Movies_method_error(self):
        res = self.client().post('/movies/1',headers=producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,405)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'])
        self.assertEqual(data['success'],False)
    
    def test_edit_Movies_request_error(self):
        res = self.client().patch('/movies/100',headers=producer_header,json={"name":"original","estimated_project_time":70,"need_actors":True})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'])
        self.assertEqual(data['success'],False)
    
    def test_Plays(self):
        res = self.client().get('/plays',headers=assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data['plays'])
    
    def test_add_Plays(self):
        res = self.client().post('/plays',headers=producer_header,json={"movies_id": 3,"actors_id":3})
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['movie_id'])
        self.assertTrue(data['actor_id'])
    
    def test_add_Plays_method_error(self):
        res = self.client().delete('/plays',headers=producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,405)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'])
        self.assertEqual(data['success'],False)
    
    def test_add_Plays_request_error(self):
        res = self.client().post('/plays',headers=producer_header,json={'movie_id':1,'actor_id':100})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,400)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'])
        self.assertEqual(data['success'],False)
    
    def test_delete_Play(self):
        res = self.client().delete('/plays/2',headers=producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data['deleted_id'])
    
    def test_delete_Plays_method_error(self):
        res = self.client().post('/plays/2',headers=producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,405)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'])
        self.assertEqual(data['success'],False)
    
    def test_delete_Plays_request_error(self):
        res = self.client().delete('/plays/50',headers=producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'])
        self.assertEqual(data['success'],False)
    
    def test_edit_Plays(self):
        res = self.client().patch('/plays/16',headers=producer_header,json={"movie_id":1,"actor_id":2})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
    
    def test_edit_Plays_method_error(self):
        res = self.client().post('/plays/4',headers=director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,405)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'])
        self.assertEqual(data['success'],False)
    
    def test_edit_Plays_request_error(self):
        res = self.client().patch('/plays/10',headers=producer_header,json={"movie_id":1,"actor_id":3})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'])
        self.assertEqual(data['success'],False)

if __name__ == "__main__":
    unittest.main()
    

    

