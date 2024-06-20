from flask import Blueprint, render_template, request
import psycopg2

auth = Blueprint('auth', __name__)

@auth.route('/signin')
def signin():
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
        cur.execute(f"SELECT user.id, user.email FROM user WHERE user.email = {email};")
        data = cur.fetchall()
        if(len(data) > 0):
            # flash('Email already exists', category='error')
            print("Email already exists")
        elif len(password1) < 8:
            # flash('Password must be longer than or 7 characters', category='error')
            print("Passwrd must be longer than 8")
        elif password1 != password2:
            # flash('Passwords don\'t match', category='error')
            print("Password don't match")
        else:
            cur.execute('INSERT INTO client (email, password, NAS, nom, addresse, card_number)'
                'VALUES (%s, %s, %s, %s, %s, %s)',
                (f'{name}',
                f'{email}',
                f'{password1}')
                )
            print("User added")
            conn.commit()
            cur.close() 
            conn.close()


    return render_template("signup.html")

#Function to connect to the database
def connect_db():
    conn = psycopg2.connect(
            host = "localhost",
            database = "project_db",
            user = "manager",
            port = "5432",
            password = "Mon12345")
    return conn