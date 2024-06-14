from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)

@auth.route('/signin')
def signin():
    return render_template("signin.html")