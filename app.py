from flask import Flask
from config import Config
from models import db
from routes import EcommerceRoutes

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db.init_app(app)

# Register OOP Routes
EcommerceRoutes(app)

# Create database tables (run only first time)
with app.app_context():
    db.create_all()
    
# if __name__ == '__main__':
#     app.run(debug=True)