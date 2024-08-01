from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
import psycopg2

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template("index.html")

@views.route('/home', methods = ['GET','POST'])
@login_required
def home():
    conn = connect_db()
    cur = conn.cursor()

    if request.method == 'POST':
        project_id = int(request.form['project_id'])
        # cur.execute(f"SELECT * FROM projects WHERE projects.project_id = '{project_id}';")
        # project = cur.fetchall()
        # print("****************home()")
        # print(type(project))
        # print(project)
        return redirect(url_for('views.project', project_id = project_id))
    else :
        cur.execute(f"SELECT * FROM projects WHERE projects.user_id = '{current_user.id}';")
        projects = cur.fetchall()
        print(type(projects))
        print(f"**************************************{projects}")
        length = len(projects)
        return render_template("home.html", user = current_user, projects = projects, length = length)

@views.route('/proj')
@login_required
def project():
    project_id = request.args.get('project_id')
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM projects WHERE projects.project_id = {project_id};")
    project = cur.fetchall()
    
    print("*********************project()")
    print(type(project))
    print(project)

    cur.execute(f"SELECT tasks.id, tasks.description, tasks.done FROM projects INNER JOIN tasks ON projects.project_id = {project_id} AND tasks.project_id = projects.project_id;")
    tasks = cur.fetchall()
    print()
    print("*********************project()")
    length = len(tasks)
    print(type(tasks))
    print(tasks)

    return render_template("project.html", tasks = tasks, user = current_user, project = project, length = length)

@views.route('/create-project', methods = ['GET','POST'])
@login_required
def create_project():
    if request.method == "POST":
        title = request.form.get("title")
        conn = connect_db()
        cur = conn.cursor()
        cur.execute('INSERT INTO projects (user_id, title)'
                'VALUES (%s, %s)',
                (f'{current_user.id}',
                f'{title}')
                )
        conn.commit()
        cur.close() 
        conn.close()
        return redirect(url_for("views.home"))
    return render_template("create.html", user = current_user)

#Function to connect to the database
def connect_db():
    conn = psycopg2.connect(
            host = "localhost",
            database = "project_db",
            user = "postgres",
            port = "5432",
            password = "berserk")
    return conn