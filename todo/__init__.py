import os
from flask import Flask

def create_app():
  app = Flask(__name__)
  #env variables
  app.config.from_mapping(
          SECRET_KEY="MyExampleKey",
          DATABASE_HOST=os.environ.get('FLASK_DATABASE_HOST'),
          DATABASE_PASSWORD=os.environ.get('FLASK_DATABASE_PASSWORD'),
          DATABASE_USER=os.environ.get('FLASK_DATABASE_USER'),
          DATABASE=os.environ.get('FLASK_DATABASE')
  )        

  #import the db module and call the init_app function passing out app
  from . import db
  db.init_app(app)
  
  #inscribimos nuestro blueprint
  from . import auth
  app.register_blueprint(auth.bp)

  #inscribimos el blueprint de los todos
  from . import todo
  app.register_blueprint(todo.bp)   
 
  return app
