from flask import Blueprint, render_template, request, flash, redirect, url_for
import psycopg2
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    if request.method == 'POST':
        
        email = request.form.get("email")
        password = request.form.get("password")

        conn = connect_db()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM users WHERE users.email = '{email}';")
        data = cur.fetchall()
        print("Data is")
        print(data)


        if(len(data) < 1):
            flash('Email doesn\'t exist', category = 'error')
        elif not (check_password_hash(data[0][3], password)):
            flash('Email and password don\'t match', category='error')
        else:
            user = User(data[0][0], data[0][1], data[0][2], data[0][3])
            login_user(user, remember = True)
            return redirect(url_for('views.home'))

    return render_template("signin.html")

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        
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
            hash = generate_password_hash(password1, method='sha256')
            cur.execute('INSERT INTO users (name, email, password)'
                'VALUES (%s, %s, %s)',
                (f'{name}',
                f'{email}',
                f'{hash}')
                )
            conn.commit()
            cur.close() 
            conn.close()
            flash('Account created succesfully', category = 'success')


    return render_template("signup.html")

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.signin'))

#Function to connect to the database
def connect_db():
    conn = psycopg2.connect(
            host = "localhost",
            database = "project_db",
            user = "postgres",
            port = "5432",
            password = "berserk")
    return conn