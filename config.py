class Config:
    SECRET_KEY = 'your_secret_key_here'  # Change this
    SQLALCHEMY_DATABASE_URI = 'sqlite:///ecommerce.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
