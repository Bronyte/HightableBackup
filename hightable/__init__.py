from flask import Flask
from flask_login import LoginManager
from dotenv import load_dotenv
from .db import db
from hightable.models import User
import os

load_dotenv()
login_manager = LoginManager()


def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY'] = 'alpha bock'

  app.config[
      'SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}?ssl_ca=/etc/ssl/certs/ca-certificates.crt"

  db.init_app(app)

  from .views import views
  from .auth import auth

  app.register_blueprint(views, url_prefix='/')
  app.register_blueprint(auth, url_prefix='/')
  
  login_manager.login_view = 'auth.login'
  login_manager.init_app(app)

  @login_manager.user_loader
  def load_user(user_id):
    user = User.get(user_id)
    return user
  return app
