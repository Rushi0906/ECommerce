from flask import Flask,request, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Product, Seller
import os
from werkzeug.utils import secure_filename
from flask_migrate import Migrate


app = Flask(__name__)
app.secret_key = "mysecretkey123" 
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql+pymysql://root:1111@localhost/ecommerce'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# ============================================================================================
class Seller(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    storename = db.Column(db.String(100), nullable=False)
    ownername = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)  # Must be unique
    phone = db.Column(db.String(20), nullable=False)
    gst = db.Column(db.String(30), nullable=False, unique=True)     # Must be unique
    desc = db.Column(db.Text)                                        # Seller description


@app.route("/register_seller", methods=['GET', 'POST'])
def register_seller():
    if (request.method =='POST'):
        '''add entry to the database'''
        storename = request.form.get('storename')
        ownername = request.form.get('ownername')
        email = request.form.get('email')
        phone = request.form.get('phone')
        gst = request.form.get('gst')
        desc = request.form.get('desc')

        entry = Seller(storename=storename, ownername=ownername, email=email, phone=phone, gst=gst, desc=desc)
        db.session.add(entry)
        db.session.commit()

        return redirect(url_for('success'))

    return render_template('seller.html')
# ===================================================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

@app.route('/sign', methods=['GET','POST'])
def sign():
    if(request.method == 'POST'):
        '''ADD ENTRY TO DATABASE'''
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Create new user object
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        if user:
            # Store user session
            session['user_id'] = user.id
            session['username'] = user.username
            print(f"Welcome back, {user.username}!", "success")
            # Redirect to shop page after login
            return redirect(url_for('shop'))
        else:
            print("Invalid email or password.", "danger")
            return redirect(url_for('sign'))
    
    return render_template('sign.html')
# =================================================
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    old_price = db.Column(db.Float)       # Optional: original price before discount
    discount = db.Column(db.Float)        # Optional: discount percentage
    rating = db.Column(db.Integer)        # Optional: product rating
    image = db.Column(db.String(200))     # Path to product image
    description = db.Column(db.Text)      # Product description

    seller_id = db.Column(db.Integer, db.ForeignKey('seller.id'), nullable=False)

    is_approved = db.Column(db.Boolean, default=False)  # <--- Added approval status

    seller = db.relationship('Seller', backref=db.backref('products', lazy=True))

@app.route('/add_product', methods=['GET','POST'])
def add_product():
        if(request.method == 'POST'):
            '''ADD ENTRY TO DATABASE'''
            name = request.form['productName']
            price = float(request.form['productPrice'])
            description = request.form.get('productDescription', '')
            category = request.form.get('productCategory', '')

            image_file = request.files.get('productImage')
            image_path = ''
            if image_file and image_file.filename != '':
                filename = secure_filename(image_file.filename)
                image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_path = f'Uploads/{filename}'

            new_product = Product(
            name=name,
            category=category,
            price=price,
            description=description,
            image=image_path,
            is_approved=False 
            )

            
            db.session.add(new_product)
            db.session.commit()
            print('Product added successfully!', 'success')
        return render_template('admin.html')
# ======================================================
@app.route('/admin/products/pending')
def pending_products():
    pending = Product.query.filter_by(is_approved=False).all()
    return render_template('pending_products.html', products=pending)
# ===============================================================
@app.route('/admin/product/approve/<int:product_id>', methods=['POST'])
def approve_product(product_id):
    product = Product.query.get_or_404(product_id)
    product.is_approved = True
    db.session.commit()
    return redirect(url_for('pending_products'))

# ===============================================
@app.route("/success")
def success():
    return "✅ Seller Registered Successfully!"

# =================================================
@app.route('/')
def home():
    # products = Product.query.limit(4).all()
    return render_template('index.html')
# ==============================================
@app.route('/shop')
def shop():
    # products = Product.query.filter_by(is_approved=True).all()
    return render_template('shop.html')
# =============================================
@app.route('/product/<int:id>')
def product_detail(id):
    #product = Product.query.get_or_404(id)
    return render_template('productpage.html')
#====================================
@app.route('/contact')
def contact():
    return render_template('contact.html')
# ================================
@app.route('/seller')
def seller():
    return render_template('seller.html')
#=================================
@app.route('/forgotpassword')
def forgotpassword():
    return render_template('forgotpassword.html')
# ========================================
@app.route('/signup')
def signup():
    return render_template('sign up')
# ========================================
@app.route('/logout')
def logout():
    return "logout"
#=====================================
@app.route('/admin', methods=['GET'])
def admin():
    return "admin"
# ==========================================
# @app.route('/add_product', methods=['POST'])
# def add_product():
#     return "add products"
# =======================================
@app.route('/delete_product')
def delete_product():
    return "delete products"

# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True)


