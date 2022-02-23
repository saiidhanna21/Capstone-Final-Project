import os
from sqlalchemy import Column, Integer,String, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Person
Have title and release year
'''
class Actor(db.Model):  
  __tablename__ = 'Actors'

  id = Column(db.Integer, primary_key=True)
  name = Column(String(30))
  age = Column(Integer)
  career = Column(String(80))
  projects = Column(String(300))
  experience = Column(Integer,nullable=False)
  plays = db.relationship('Play',backref='movies',lazy=True)

  def __init__(self, name, age, career, projects, experience):
    self.name = name
    self.age = age
    self.career = career
    self.projects = projects
    self.experience = experience

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def update(self):
    db.session.commit()

  def rollback():
    db.session.rollback()

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'age':self.age,
      'career':self.career,
      'projects':self.projects,
      'experience':self.experience,
      }

class Movie(db.Model):
    __tablename__='Movies'
    id = Column(Integer,primary_key=True)
    name = Column(String)
    estimated_project_time = Column(Integer,nullable=False)
    need_actors = Column(db.Boolean,default=False)
    movie = db.relationship('Play',backref='actors',lazy=True)

    def __init__(self, name, estimated_project_time, need_actors):
      self.name = name
      self.estimated_project_time = estimated_project_time
      self.need_actors = need_actors

    def insert(self):
      db.session.add(self)
      db.session.commit()
    
    def delete(self):
      db.session.delete(self)
      db.session.commit()

    def update(self):
      db.session.commit()
    
    def rollback():
      db.session.rollback()

    def format(self):
      return {
        'id': self.id,
        'name': self.name,
        'estimated_project_time':self.estimated_project_time,
        'need_actors':self.need_actors,
      }
class Play(db.Model):
    __tablename__='plays'
    
    id = Column(Integer,primary_key=True)
    movies_id = Column(Integer,db.ForeignKey('Movies.id'),nullable=False)
    actors_id = Column(Integer,db.ForeignKey('Actors.id'),nullable=False)

    def __init__(self, movies_id, actors_id):
      self.movies_id = movies_id 
      self.actors_id = actors_id
    
    def insert(self):
      db.session.add(self)
      db.session.commit()
    
    def delete(self):
      db.session.delete(self)
      db.session.commit()

    def update(self):
      db.session.commit()
    
    def rollback():
      db.session.rollback()
    
    def format(self):
        return {
        'id': self.id,
        'movie_id': self.movies_id,
        'actor_id':self.actors_id,
      }

