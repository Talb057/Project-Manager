from flask import Flask
import psycopg2
from flask_login import LoginManager

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'miftah dar'

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')

    from .models import User

    login_manager = LoginManager()
    login_manager.login_view = 'auth.signin'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        conn = connect_db()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM users WHERE users.user_id = '{id}';")
        data = cur.fetchall()
        user = User(data[0][0], data[0][1], data[0][2], data[0][3])
        return user

    print("*************************************8888")

    return app

def connect_db():
    conn = psycopg2.connect(
            host = "localhost",
            database = "project_db",
            user = "postgres",
            port = "5432",
            password = "berserk")
    
    return conn