# routes/auth_routes.py
from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from database import db
from models.user_model import User

bcrypt = Bcrypt()  # bound in app via record_once

auth_routes = Blueprint("auth_routes", __name__)

@auth_routes.record_once
def on_load(setup_state):
    bcrypt.init_app(setup_state.app)

@auth_routes.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    hashed_pw = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    new_user = User(name=data["name"], email=data["email"], password=hashed_pw, role=data.get("role", "student"))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "User registered successfully"})

@auth_routes.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data["email"]).first()
    if user and bcrypt.check_password_hash(user.password, data["password"]):
        token = create_access_token(identity={"id": user.id, "role": user.role})
        return jsonify({"token": token, "name": user.name, "role": user.role})
    return jsonify({"msg": "Invalid credentials"}), 401
