# models/user_model.py
from database import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), default="student")

    def __init__(self, name, email, password, role="student"):
        self.name = name
        self.email = email
        self.password = password
        self.role = role
