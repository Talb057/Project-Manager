from . import db
from flask_login import UserMixin
# from sqlalchemy.sql import func

class User(UserMixin):
    def __init__(self, id, name, email, password):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
