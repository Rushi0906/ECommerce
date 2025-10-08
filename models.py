from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# -------------------------
# User Model
# -------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

# -------------------------
# Product Model
# -------------------------
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    old_price = db.Column(db.Float)       # Optional: original price before discount
    discount = db.Column(db.Float)        # Optional: discount percentage
    rating = db.Column(db.Integer)        # Optional: product rating
    image = db.Column(db.String(200))     # Path to product image
    description = db.Column(db.Text)      # Product description

    def __repr__(self):
        return f"<Product {self.name}>"

# -------------------------
# Seller Model
# -------------------------
class Seller(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    storename = db.Column(db.String(100), nullable=False)
    ownername = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)  # Must be unique
    phone = db.Column(db.String(20), nullable=False)
    gst = db.Column(db.String(30), nullable=False, unique=True)     # Must be unique
    desc = db.Column(db.Text)                                        # Seller description

    def __repr__(self):
        return f"<Seller {self.storename}>"
