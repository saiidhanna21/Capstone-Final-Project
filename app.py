from operator import ne
import os
from flask import Flask,json,jsonify,abort,request
import sqlalchemy
from auth import requires_auth
from models import Actor, Movie, Play,setup_db,db
from flask_cors import CORS
import sys

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def get_greeting():
        excited = os.environ['EXCITED']
        greeting = "Hello" 
        if excited == 'true': 
            greeting = greeting + "!!!!! You are doing great in this Udacity project."
        return greeting
   
    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actor(payload):
        try:
            data = Actor.query.order_by('id').all()
            actors = [actor.format() for actor in data]
            return jsonify({
                "actors":actors,
            })
        except Exception:
            abort(401)

    @app.route('/actors/<int:actors_id>')
    @requires_auth('get:actors')
    def get_actor_byId(payload,actors_id):
        try:
            actor = Actor.query.filter(Actor.id==actors_id).one_or_none()
            return jsonify({
                'id':actor.id,
                'name':actor.name,
                'age':actor.age,
                'career':actor.career,
                'projects':actor.projects,
                'experience':actor.experience,
            })
        except AttributeError:
            abort(404)
    @app.route('/actors',methods=['POST'])
    @requires_auth('post:actors')
    def add_actors(payload):
        body = request.get_json()
        try:
            new_name = body.get('name')
            new_age = body.get('age')
            new_career = body.get('career')
            new_projects = body.get('projects')
            new_experience = body.get('experience')

            actor = Actor(name=new_name,age=new_age,career=new_career,projects=new_projects,experience=new_experience)
            actor.insert()
            return jsonify({
                'actor_added':actor.format(),
            })     
        
        except sqlalchemy.exc.IntegrityError:
            Actor.rollback()
            abort(400)
        
        except Exception:
            Actor.rollback()
            abort(405)
    
    @app.route('/actors/<int:id>',methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload,id):
        try:
            actor = Actor.query.filter(Actor.id==id).one_or_none()
            actor.delete()            
            return jsonify({
                'deleted_id':actor.id,
            })
        except AttributeError:
            Actor.rollback()
            abort(404)

        except Exception:
            Actor.rollback()
            abort(405)
    
    @app.route('/actors/<int:actor_id>',methods=['PATCH'])
    @requires_auth('patch:actors')
    def actor_update(payload,actor_id):
        body = request.get_json()
        try:
            actor = Actor.query.filter(Actor.id==actor_id).first()
            actor.name = body.get('name')
            actor.age = body.get('age')
            actor.career = body.get('career')
            actor.projects = body.get('projects')
            actor.experience = body.get('experience')
            
            Actor.update(actor)
            return jsonify({
                "updated_actor":actor.format(),
            })
        except AttributeError:
            Actor.rollback()
            abort(404)

        except Exception:
            Actor.rollback()
            abort(405)

    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(payload):
        try:
            data = Movie.query.order_by('id').all()
            movies = [movie.format() for movie in data]
            return jsonify({
                "movies":movies,
            })
        except Exception:
            abort(401)
    
    @app.route('/movies/<int:movie_id>')
    @requires_auth('get:movies')
    def get_movie_byId(payload,movie_id):
        try:
            movie = Movie.query.filter(Movie.id==movie_id).one_or_none()
            return jsonify({
                'id': movie.id,
                'name': movie.name,
                'estimated_project_time':movie.estimated_project_time,
                'need_actors':movie.need_actors,
            })
        except AttributeError:
            abort(404)
    
    @app.route('/movies',methods=['POST'])
    @requires_auth('post:movies')
    def add_movies(payload):
        body = request.get_json()
        try:
            new_name = body.get('name')
            new_release_date = body.get('estimated_project_time')
            new_need_actors = body.get('need_actors')

            movie = Movie(name=new_name,estimated_project_time=new_release_date,need_actors=new_need_actors)
            movie.insert()
            return jsonify({
                'movie_added':movie.format(),
            })     
        
        except sqlalchemy.exc.IntegrityError:
            Movie.rollback()
            abort(400)
        
        except Exception:
            Movie.rollback()
            abort(405)
    
    @app.route('/movies/<int:id>',methods=['DELETE'])        
    @requires_auth('delete:movies')
    def delete_movie(payload,id):
        try:
            movie = Movie.query.filter(Movie.id==id).one_or_none()
            movie.delete()            
            return jsonify({
                'deleted_id':movie.id,
            })
        except AttributeError:
            Movie.rollback()
            abort(404)

        except Exception:
            Movie.rollback()
            abort(405)
    
    @app.route('/movies/<int:movie_id>',methods=['PATCH'])
    @requires_auth('patch:movies')
    def movie_update(payload,movie_id):
        body = request.get_json()
        try:
            movie = Movie.query.filter(Movie.id==movie_id).first()
            movie.name = body.get('name')
            movie.estimated_projet_time = body.get('estimated_project_time')
            movie.need_actors = body.get('need_actors')
            
            Movie.update(movie)
            return jsonify({
                "updated_movie":movie.format(),
            })
        except AttributeError:
            Movie.rollback()
            abort(404)

        except Exception:
            Movie.rollback()
            abort(405)

    @app.route('/plays')
    @requires_auth('get:plays')
    def get_plays(payload):
        try:
            data = db.session.query(Play,Actor,Movie).join(Actor,Movie).order_by('id').all()
            plays = [{"id":play.Play.id,"movie_id":play.Movie.id,"actor_id":play.Actor.id} for play in data]
            return jsonify({
                "plays":plays,
            })
        except Exception:
            print(sys.exc_info)
            abort(401)
    
    @app.route('/plays',methods=['POST'])
    @requires_auth('post:plays')
    def add_play(payload):
        body = request.get_json()
        try:
            new_movie_id = body.get('movies_id')
            new_actor_id = body.get('actors_id')

            play = Play(movies_id=new_movie_id,actors_id=new_actor_id)
            play.insert()

            return jsonify({
                'id': play.id,
                'movie_id': play.movies_id,
                'actor_id':play.actors_id,
        })
        except sqlalchemy.exc.IntegrityError:
            Play.rollback()
            abort(400)
        
        except Exception:
            Play.rollback()
            abort(405)

    @app.route('/plays/<int:id>',methods=['PATCH'])
    @requires_auth('patch:plays')
    def update_plays(payload,id):
        body = request.get_json()
        try:
            play = db.session.query(Play,Actor,Movie).join(Actor,Movie).filter(Play.id==id).first()
            play.movies_id = body.get('movie_id')
            play.actors_id = body.get('actor_id')
            Play.update(play)

            return jsonify({
                'success':True,
            })
                
        except AttributeError:
            Play.rollback()
            abort(404)
        
        except Exception:
            Play.rollback()
            abort(405)  
    
    @app.route('/plays/<int:id>',methods=['DELETE'])
    @requires_auth('delete:plays')
    def delete_plays(payload,id):
        try:
            play = Play.query.filter(Play.id==id).one_or_none()
            play.delete()
            return jsonify({
                'deleted_id':play.id,
            })
        except AttributeError:
            Play.rollback()
            abort(404)

        except Exception:
            Play.rollback()
            abort(405)

    @app.errorhandler(404)
    def not_found(error):
        return(jsonify({
            'success':False,
            'message':'The page was not found, please Try again',
            'error':'404',
        })
        ,404
        )
    
    @app.errorhandler(405)
    def Method_Not_Allowed(error):
        return (jsonify({
            'success':False,
            'error':'405',
            'message':'Method not allowed'
        })
        ,405
        )
    @app.errorhandler(400)
    def server_cannot_process(error):
        return (jsonify({
            'success':False,
            'error':'400',
            'message':'server cannot process due to malformed request syntax or invalid request'
        })
        ,400
        )
    @app.errorhandler(401)
    def unauthorized_response(error):
        return (jsonify({
            'success':False,
            'error':'401',
            'message':'Lacks valid authentication credentials for the requested resource'
        })
        ,401
        )

    return app
    

app = create_app()

if __name__ == '__main__':
    app.run()
