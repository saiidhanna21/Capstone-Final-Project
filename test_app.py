import os
from sre_constants import SUCCESS
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import delete
from auth import requires_auth
from app import create_app
from models import setup_db, Actor, Movie, Play


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
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data['actors'])
    
    def test_Actors_id(self):
        res = self.client().get('/actors/10')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data['name'])
        self.assertTrue(data['age'])
        self.assertTrue(data['career'])
        
    def test_Actors_id_error(self):
        res = self.client().get('/actors/100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'])
        self.assertEqual(data['success'],False)
    
    def test_add_Actors(self):
        res = self.client().post('/actors',json={"name":"joe","age":20,"career":"drama","projects":"","experience":0})
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
        res = self.client().post('/actors',json={'name':'saiid'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,400)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'])
        self.assertEqual(data['success'],False)
    
    def test_delete_Actor(self):
        res = self.client().delete('/actors/3')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data['deleted_id'])
    
    def test_delete_Actors_method_error(self):
        res = self.client().post('/actors/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,405)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'])
        self.assertEqual(data['success'],False)
    
    def test_delete_Actors_request_error(self):
        res = self.client().delete('/actors/50')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'])
        self.assertEqual(data['success'],False)
    
    def test_edit_Actors(self):
        res = self.client().patch('/actors/1',json={"name":"joe","age":20,"career":"drama","projects":"","experience":5})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data['updated_actor'])
    
    def test_edit_Actors_method_error(self):
        res = self.client().post('/actors/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,405)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'])
        self.assertEqual(data['success'],False)
    
    def test_edit_Actors_request_error(self):
        res = self.client().patch('/actors/100',json={"name":"joe","age":20,"career":"drama","projects":"","experience":5})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'])
        self.assertEqual(data['success'],False)
    
    def test_Movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data['movies'])
    
    def test_Movies_id(self):
        res = self.client().get('/movies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data['name'])
        self.assertTrue(data['estimated_project_time'])
        self.assertTrue(data['need_actors'])
        
    def test_Movies_id_error(self):
        res = self.client().get('/movies/100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'])
        self.assertEqual(data['success'],False)
    
    def test_add_Movies(self):
        res = self.client().post('/movies',json={"name":"original","estimated_project_time":70,"need_actors":True})
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['movie_added'])
    
    def test_add_Moives_method_error(self):
        res = self.client().delete('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,405)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'])
        self.assertEqual(data['success'],False)
    
    def test_add_Movies_request_error(self):
        res = self.client().post('/movies',json={'name':'saiid'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,400)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'])
        self.assertEqual(data['success'],False)
    
    def test_delete_Movie(self):
        res = self.client().delete('/movies/2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data['deleted_id'])
    
    def test_delete_Movies_method_error(self):
        res = self.client().post('/movies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,405)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'])
        self.assertEqual(data['success'],False)
    
    def test_delete_Movies_request_error(self):
        res = self.client().delete('/movies/50')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'])
        self.assertEqual(data['success'],False)
    
    def test_edit_Movies(self):
        res = self.client().patch('/movies/1',json={"name":"original","estimated_project_time":70,"need_actors":True})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data['updated_movie'])
    
    def test_edit_Movies_method_error(self):
        res = self.client().post('/movies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,405)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'])
        self.assertEqual(data['success'],False)
    
    def test_edit_Movies_request_error(self):
        res = self.client().patch('/movies/100',json={"name":"original","estimated_project_time":70,"need_actors":True})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'])
        self.assertEqual(data['success'],False)
    
    def test_Plays(self):
        res = self.client().get('/plays')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data['plays'])
    
    def test_add_Plays(self):
        res = self.client().post('/plays',json={"movies_id": 3,"actors_id":3})
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['movie_id'])
        self.assertTrue(data['actor_id'])
    
    def test_add_Plays_method_error(self):
        res = self.client().delete('/plays')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,405)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'])
        self.assertEqual(data['success'],False)
    
    def test_add_Plays_request_error(self):
        res = self.client().post('/plays',json={'movie_id':1,'actor_id':100})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,400)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'])
        self.assertEqual(data['success'],False)
    
    def test_delete_Play(self):
        res = self.client().delete('/plays/2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data['deleted_id'])
    
    def test_delete_Plays_method_error(self):
        res = self.client().post('/plays/2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,405)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'])
        self.assertEqual(data['success'],False)
    
    def test_delete_Plays_request_error(self):
        res = self.client().delete('/plays/50')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'])
        self.assertEqual(data['success'],False)
    
    def test_edit_Plays(self):
        res = self.client().patch('/plays/16',json={"movie_id":1,"actor_id":2})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
    
    def test_edit_Plays_method_error(self):
        res = self.client().post('/plays/4')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,405)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'])
        self.assertEqual(data['success'],False)
    
    def test_edit_Plays_request_error(self):
        res = self.client().patch('/plays/10',json={"movie_id":1,"actor_id":3})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'])
        self.assertEqual(data['success'],False)

if __name__ == "__main__":
    unittest.main()
    

    

