# routes/feedback_routes.py
from flask import Blueprint, request, jsonify
from database import db
from models.feedback_model import Feedback

print("Loaded feedback_routes")  # dev diagnostic

feedback_routes = Blueprint("feedback_routes", __name__)

@feedback_routes.route("", methods=["POST"])
def submit_feedback():
    data = request.get_json()
    fb = Feedback(user=data["user"], rating=int(data["rating"]), comment=data["comment"])
    db.session.add(fb)
    db.session.commit()
    return jsonify({"msg": "Feedback submitted"})

@feedback_routes.route("", methods=["GET"])
def get_feedback():
    feedbacks = Feedback.query.all()
    result = [
        {"id": f.id, "user": f.user, "comment": f.comment, "rating": f.rating}
        for f in feedbacks
    ]
    return jsonify(result)
