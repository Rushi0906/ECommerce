from flask import Flask, render_template, redirect, url_for, request, flash, session
from models import db, User, Product, Seller
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/Uploads'

class EcommerceRoutes:
    def __init__(self, app: Flask):
        self.app = app
        self.app.secret_key = 'your-secret-key'  # Required for session
        self.app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        self.register_routes()

    def register_routes(self):
        # -------------------------
        # Home Page
        # -------------------------
        @self.app.route('/')
        def home():
            products = Product.query.limit(4).all()
            return render_template('index.html', products=products)

        # -------------------------
        # Shop Page
        # -------------------------
        @self.app.route('/shop')
        def shop():
            products = Product.query.all()
            return render_template('shop.html', products=products)

        # -------------------------
        # Product Detail Page
        # -------------------------
        @self.app.route('/product/<int:id>')
        def product_detail(id):
            product = Product.query.get_or_404(id)
            return render_template('productpage.html', product=product)

        # -------------------------
        # Contact Page
        # -------------------------
        @self.app.route('/contact')
        def contact():
            return render_template('contact.html')

        # -------------------------
        # Signup
        # -------------------------
        @self.app.route('/signup', methods=['GET', 'POST'])
        def signup():
            if request.method == 'POST':
                username = request.form.get('username')
                email = request.form.get('email')
                password = request.form.get('password')
                confirm = request.form.get('confirm')

                # Password confirmation
                if password != confirm:
                    flash("Passwords do not match.", "danger")
                    return redirect(url_for('signup'))

                # Check if user exists
                if User.query.filter_by(email=email).first():
                    flash("Email already registered. Please login.", "danger")
                    return redirect(url_for('signup'))

                # Create new user
                new_user = User(username=username, email=email, password=password)
                try:
                    db.session.add(new_user)
                    db.session.commit()
                    flash("Signup successful! Please login.", "success")
                    return redirect(url_for('sign'))
                except Exception as e:
                    db.session.rollback()
                    flash(f"Error: {str(e)}", "danger")
                    return redirect(url_for('signup'))

            return render_template('signup.html')

        # -------------------------
        # Signin
        # -------------------------
        @self.app.route('/sign', methods=['GET', 'POST'])
        def sign():
            if request.method == 'POST':
                email = request.form.get('email')
                password = request.form.get('password')

                user = User.query.filter_by(email=email, password=password).first()
                if user:
                    # Store user session
                    session['user_id'] = user.id
                    session['username'] = user.username
                    flash(f"Welcome back, {user.username}!", "success")
                    # Redirect to shop page after login
                    return redirect(url_for('shop'))
                else:
                    flash("Invalid email or password.", "danger")
                    return redirect(url_for('sign'))

            return render_template('sign.html')

        # -------------------------
        # Logout
        # -------------------------
        @self.app.route('/logout')
        def logout():
            session.clear()
            flash("You have been logged out.", "success")
            return redirect(url_for('sign'))

        # -------------------------
        # Admin Dashboard
        # -------------------------
        @self.app.route('/admin', methods=['GET'])
        def admin():
            products = Product.query.all()
            return render_template('admin.html', products=products)

        # -------------------------
        # Add Product
        # -------------------------
        @self.app.route('/add_product', methods=['POST'])
        def add_product():
            name = request.form['productName']
            price = float(request.form['productPrice'])
            description = request.form.get('productDescription', '')
            category = request.form.get('productCategory', '')

            image_file = request.files.get('productImage')
            image_path = ''
            if image_file and image_file.filename != '':
                filename = secure_filename(image_file.filename)
                image_file.save(os.path.join(self.app.config['UPLOAD_FOLDER'], filename))
                image_path = f'Uploads/{filename}'

            new_product = Product(
                name=name,
                price=price,
                description=description,
                category=category,
                image=image_path
            )
            db.session.add(new_product)
            db.session.commit()
            flash('Product added successfully!', 'success')
            return redirect(url_for('admin'))

        # -------------------------
        # Delete Product
        # -------------------------
        @self.app.route('/delete_product/<int:id>', methods=['POST'])
        def delete_product(id):
            product = Product.query.get_or_404(id)
            db.session.delete(product)
            db.session.commit()
            flash('Product deleted successfully!', 'success')
            return redirect(url_for('admin'))

        # -------------------------
        # Seller Page
        # -------------------------
        @self.app.route('/seller')
        def seller():
            return render_template('seller.html')

        # -------------------------
        # Seller Registration
        # -------------------------
        @self.app.route('/register_seller', methods=['POST'])
        def register_seller():
            storename = request.form.get('storename')
            ownername = request.form.get('ownername')
            email = request.form.get('email')
            phone = request.form.get('phone')
            gst = request.form.get('gst')
            desc = request.form.get('desc')

            # Check for duplicate email
            if Seller.query.filter_by(email=email).first():
                flash("Email already registered. Please use another email.", "danger")
                return redirect(url_for('seller'))

            new_seller = Seller(
                storename=storename,
                ownername=ownername,
                email=email,
                phone=phone,
                gst=gst,
                desc=desc
            )

            try:
                db.session.add(new_seller)
                db.session.commit()
                flash("Seller registered successfully!", "success")
            except Exception as e:
                db.session.rollback()
                flash(f"Error: {str(e)}", "danger")

            return redirect(url_for('seller'))
