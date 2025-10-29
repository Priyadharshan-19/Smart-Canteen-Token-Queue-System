# app.py
from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from database import db, init_menu_db, DB_PATH
import os, sys

app = Flask(__name__, static_folder=None)

# Ensure instance folder exists (for SQLite)
os.makedirs(os.path.join(os.path.dirname(__file__), "instance"), exist_ok=True)

# Database and JWT config
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "supersecret"  # change in production

# CORS for API routes (development-friendly)
CORS(
    app,
    resources={r"/api/*": {"origins": "*"}},
    supports_credentials=False,
    allow_headers=["Content-Type", "Authorization"],
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
)

# Initialize extensions
db.init_app(app)
bcrypt = Bcrypt(app)
JWTManager(app)

# Import blueprints AFTER app/extensions are set up
from routes.auth_routes import auth_routes
from routes.order_routes import order_routes
from routes.feedback_routes import feedback_routes

# Register blueprints (NO trailing slashes)
app.register_blueprint(auth_routes, url_prefix="/api/auth")
app.register_blueprint(order_routes, url_prefix="/api/orders")
app.register_blueprint(feedback_routes, url_prefix="/api/feedback")

# Diagnostics (okay to keep during dev)
print("Running app from:", os.path.abspath(__file__))
print("Sys.path[0]:", sys.path[0])
print("Blueprints loaded:", list(app.blueprints.keys()))

# Serve frontend
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "frontend")

@app.route("/")
def serve_index():
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        return send_from_directory(FRONTEND_DIR, "index.html")
    return {"message": "✅ Smart Canteen API Running Successfully"}

@app.route("/frontend/<path:filename>")
def serve_frontend_assets(filename):
    return send_from_directory(FRONTEND_DIR, filename)

# Create tables and init menu
with app.app_context():
    db.create_all()
    init_menu_db()
    print("✅ Database and tables initialized successfully!")

if __name__ == "__main__":
    app.run(debug=True)
