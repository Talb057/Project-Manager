from flask import Flask
import psycopg2

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'miftah dar'

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')

    return app

def connect_db():
    conn = psycopg2.connect(
            host = "localhost",
            database = "project_db",
            user = "manager",
            port = "5432",
            password = "Mon12345")
    
    return conn