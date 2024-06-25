from flask import Blueprint, render_template, request, flash
import psycopg2

auth = Blueprint('auth', __name__)

@auth.route('/signin')
def signin():
    return render_template("signin.html")

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.form
        print(data)
        
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        name = request.form.get("name")
        
        conn = connect_db()
        cur = conn.cursor()
        cur.execute(f"SELECT users.user_id, users.email FROM users WHERE users.email = '{email}';")
        data = cur.fetchall()
        if(len(data) > 0):
            flash('Email already exists', category='error')
        elif len(password1) < 8:
            flash('Password must be longer than or 8 characters', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        else:
            cur.execute('INSERT INTO users (name, email, password)'
                'VALUES (%s, %s, %s)',
                (f'{name}',
                f'{email}',
                f'{password1}')
                )
            flash('Account created succesfully', category = 'success')
            conn.commit()
            cur.close() 
            conn.close()


    return render_template("signup.html")

#Function to connect to the database
def connect_db():
    conn = psycopg2.connect(
            host = "localhost",
            database = "project_db",
            user = "postgres",
            port = "5432",
            password = "berserk")
    return conn