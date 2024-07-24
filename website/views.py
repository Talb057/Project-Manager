from flask import Blueprint, render_template
from flask_login import login_user, login_required, logout_user, current_user
import psycopg2

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template("index.html")

@views.route('/home')
@login_required
def home():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM projects WHERE projects.user_id = '{current_user.id}';")
    projects = cur.fetchall()
    print(type(projects))
    print(f"**************************************{projects}")
    length = len(projects)
    return render_template("home.html", user = current_user, projects = projects, length = length)

#Function to connect to the database
def connect_db():
    conn = psycopg2.connect(
            host = "localhost",
            database = "project_db",
            user = "postgres",
            port = "5432",
            password = "berserk")
    return conn