from operator import ne
import os
from flask import Flask,json,jsonify,abort,request
import sqlalchemy
from models import Actor, Movie, Play,setup_db
from flask_cors import CORS

# movie = Movie(name="fast",estimated_project_time="60",need_actors=True)
# movie.insert()

# play = Play(movies_id=1,actors_id=1)
# play.insert()
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
    def get_actor():
        try:
            data = Actor.query.order_by('id').all()
            actors = [actor.format() for actor in data]
            return jsonify({
                "actors":actors,
            })
        except Exception:
            abort(401)
    
    @app.route('/actors/<int:actors_id>')
    def get_actor_byId(actors_id):
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
    def add_actors():
        body = request.get_json()
        try:
            new_name = body.get('name')
            new_age = body.get('age')
            new_career = body.get('career')
            new_projects = body.get('projects')
            new_experience = body.get('experience')

            actor = Actor(name=new_name,age=new_age,career=new_career,projects=new_projects,experience=new_experience)
            actor.insert()
            x = body.get('k')
            return jsonify({
                'actor_added':actor.format(),
            })     
        
        except sqlalchemy.exc.IntegrityError:
            Actor.rollback()
            abort(400)
        
        except Exception:
            Actor.rollback()
            abort(405)
            


    @app.route('/movies')
    def get_movies():
        try:
            data = Movie.query.order_by('id').all()
            movies = [movie.format() for movie in data]
            return jsonify({
                "movies":movies,
            })
        except Exception:
            abort(401)
    
    @app.route('/movies/<int:movie_id>')
    def get_movie_byId(movie_id):
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

    @app.route('/plays')
    def get_plays():
        try:
            data = Play.query.order_by('id').all()
            plays = [play.format() for play in data]
            return jsonify({
                "plays":plays,
            })
        except Exception:
            abort(401)
    @app.route('/plays/<int:play_id>')
    def get_play_byId(play_id):
        try:
            play = Play.query.filter(Play.id==play_id).one_or_none()

            return jsonify({
                'id': play.id,
                'movie_id': play.movies_id,
                'actor_id':play.actors_id,
        })
        except AttributeError:
            abort(404)

    return app
    

app = create_app()

if __name__ == '__main__':
    app.run()
