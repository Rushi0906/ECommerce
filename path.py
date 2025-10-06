from flask import Flask, request, jsonify
from database import Seller, SessionLocal

app = Flask(__name__)

# Create a database session
def get_db():
    try:
        db = SessionLocal()
    finally:
        db.close()

# 🧱 1. CREATE Seller
@app.route("/seller", methods=["POST"])
def create_seller():
    db = next(get_db())
    data = request.get_json()

    try:
        new_seller = Seller(
            storename=data["storename"],
            ownername=data["ownername"],
            email=data["email"],
            phone=data["phone"],
            gst=data["gst"],
            desc=data.get("desc")
        )
        db.add(new_seller)
        db.commit()
        db.refresh(new_seller)
        return jsonify({"message": "Seller created successfully!", "seller": {
            "id": new_seller.id,
            "storename": new_seller.storename
        }}), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 400
    
if __name__ == "__main__":
    app.run(debug=True)