from flask import Flask, render_template, redirect, url_for, request
from models import db, User, Product

class EcommerceRoutes:
    def __init__(self, app: Flask):
        self.app = app
        self.register_routes()

    def register_routes(self):
        @self.app.route('/')
        def home():
            # Example: load first 4 products dynamically
            products = Product.query.limit(4).all()
            return render_template('index.html', products=products)

        @self.app.route('/shop')
        def shop():
            products = Product.query.all()
            return render_template('shop.html', products=products)

        @self.app.route('/contact')
        def contact():
            return render_template('contact.html')

        @self.app.route('/signup', methods=['GET', 'POST'])
        def signup():
            if request.method == 'POST':
                username = request.form['username']
                email = request.form['email']
                password = request.form['password']
                new_user = User(username=username, email=email, password=password)
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('login'))
            return render_template('signup.html')

        @self.app.route('/sign', methods=['GET', 'POST'])
        def sign():
            if request.method == 'POST':
                email = request.form['email']
                password = request.form['password']
                user = User.query.filter_by(email=email, password=password).first()
                if user:
                    return redirect(url_for('home'))
            return render_template('sign.html')

        @self.app.route('/admin')
        def admin():
            return render_template('admin.html')

        @self.app.route('/seller')
        def seller():
            return render_template('seller.html')
