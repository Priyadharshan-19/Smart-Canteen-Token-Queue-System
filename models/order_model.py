# models/order_model.py
from database import db

class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100), nullable=False)
    item = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    token_number = db.Column(db.String(50), unique=True, nullable=False)
    status = db.Column(db.String(50), default="Pending")

    def __repr__(self):
        return f"<Order {self.id} - {self.token_number}>"
