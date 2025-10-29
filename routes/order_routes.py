# routes/order_routes.py
from flask import Blueprint, request, jsonify
from database import db
from models.order_model import Order

print("Loaded order_routes")  # dev diagnostic

order_routes = Blueprint("order_routes", __name__)

@order_routes.route("", methods=["POST"])
def place_order():
    data = request.get_json()
    last_order = Order.query.order_by(Order.id.desc()).first()
    if last_order and last_order.token_number and str(last_order.token_number).isdigit():
        next_num = int(last_order.token_number) + 1
    else:
        next_num = 1
    new_order = Order(
        user=data["user"],
        item=data["item"],
        price=float(data["price"]),
        token_number=str(next_num),
        status="Pending",
    )
    db.session.add(new_order)
    db.session.commit()
    return jsonify({"msg": "Order placed", "token_number": str(next_num)})

@order_routes.route("", methods=["GET"])
def get_orders():
    orders = Order.query.all()
    result = [
        {
            "id": o.id,
            "token_number": o.token_number,
            "user": o.user,
            "item": o.item,
            "price": o.price,
            "status": o.status,
        }
        for o in orders
    ]
    return jsonify(result)

@order_routes.route("/<int:order_id>", methods=["PUT"])
def update_order(order_id):
    data = request.get_json()
    order = Order.query.get(order_id)
    if not order:
        return jsonify({"msg": "Order not found"}), 404
    order.status = data["status"]
    db.session.commit()
    return jsonify({"msg": "Status updated"})
