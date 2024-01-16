from flask import Flask, render_template, url_for, request, session, redirect, jsonify, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import shelve

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

def get_db():
    db = shelve.open('newdatabase.db', writeback=True)  # Change the filename here
    if 'users' not in db:
        print("Creating new database")
        db['users'] = {}
    return db

def close_db(db):
    db.close()

# Hardcoded staff credentials
STAFF_ID = '2468'
STAFF_PASSWORD = 'NYP2024'

@app.route('/')
def home():
    user_name = session.get('user_name', '')
    return render_template('homepage.html', user_name=user_name)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        birthday = request.form['birthday']  # Assuming it's a string

        db = get_db()
        users = db['users'] 

        if email in users:
            close_db(db)
            return render_template('signup.html', error="Email already registered.")

        hashed_password = generate_password_hash(password)
        users[email] = {'name': name, 'email': email, 'password_hash': hashed_password, 'birthday': birthday}
        db['users'] = users
        close_db(db)

        flash('You have successfully signed up!', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_type = request.form.get('user_type')
        email = request.form.get('email')
        password = request.form.get('password')

        if user_type == 'staff':
            if email == STAFF_ID and password == STAFF_PASSWORD:
                session['user_name'] = 'Staff'
                return redirect(url_for('inventory'))
            else:
                return 'Staff login failed. Please check your credentials.'
        
        elif user_type == 'member':
            db = get_db()
            users = db['users']

            user = users.get(email)
            if user and check_password_hash(user['password_hash'], password):
                session['user_name'] = user['name']
                close_db(db)
                return redirect(url_for('home'))
            else:
                close_db(db)
                flash('Login failed. Please check your credentials.')
                return redirect(url_for('login'))

    
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_name', None)
    return redirect(url_for('home'))

@app.route('/profile')
def profile():
    if 'user_name' not in session:
        return redirect(url_for('login'))
    
    db = get_db()
    users = db['users']
    user = next((u for u in users.values() if u['name'] == session['user_name']), None)

    if user:
        close_db(db)
        return render_template('edit_profile.html', user=user)
    else:
        close_db(db)
        return redirect(url_for('login'))

@app.route('/update_profile', methods=['POST'])
def update_profile():
    if 'user_name' not in session:
        return redirect(url_for('login'))

    db = get_db()
    users = db['users']
    user = next((u for u in users.values() if u['name'] == session['user_name']), None)

    if user:
        user['name'] = request.form['name']
        user['email'] = request.form['email']
        user['birthday'] = request.form['birthday']
        db['users'] = users
        close_db(db)
        return redirect(url_for('profile'))
    else:
        close_db(db)
        return redirect(url_for('login'))


@app.route('/product')
def product():
    user_name = session.get('user_name', '')  # Get the user_name from the session
    return render_template('product.html', user_name=user_name)

def get_cart_db():
    return shelve.open("cart.db")

@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    try:
        data = request.json
        product_id = str(data.get('productId'))
        quantity = data.get('quantity')


        if not product_id or quantity is None:
            return jsonify({"error": "Product ID and quantity required"}), 400


        # Retrieve product details from your products list
        product = next((p for p in products if str(p['id']) == product_id), None)


        if product:
            with get_cart_db() as db:
                if product_id in db:
                    db[product_id]['quantity'] += int(quantity)
                else:
                    db[product_id] = {
                        'product_id': product_id,
                        'quantity': int(quantity),
                        'name': product['product_name'],
                        'price': product['price'],  # Include the price here
                        'image': f"/static/{product['image']}",  # Include the full image URL here
                    }
            return jsonify({"message": "Product added to cart"}), 200
        else:
            return jsonify({"error": "Product not found"}), 404
    except Exception as e:
        app.logger.error(f"Error in add-to-cart: {e}")
        return jsonify({"error": str(e)}), 500
   

    

@app.route('/get-cart', methods=['GET'])
def get_cart():
    with get_cart_db() as db:
        cart_items = []
        for product_id, item in db.items():
            product = next((p for p in products if str(p['id']) == product_id), None)
            if product:
                cart_item = {
                    'product_id': product_id,
                    'quantity': item['quantity'],
                    'name': product.get('product_name', 'Unknown Product'),
                    'price': product.get('price', '0'),
                    'image': product.get('image', 'default.jpg')  # Fallback to default image
                }
                cart_items.append(cart_item)
            else:
                app.logger.error(f"Product with ID {product_id} not found in products list.")
        return jsonify(cart_items)




@app.route('/clear-cart', methods=['POST'])
def clear_cart():
    with get_cart_db() as db:
        db.clear()
    return jsonify({"message": "Cart cleared"}), 200


@app.route('/update-quantity', methods=['POST'])
def update_quantity():
    try:
        data = request.json
        product_id = str(data.get('productId'))
        new_quantity = int(data.get('quantity', 0))


        with get_cart_db() as db:
            if product_id in db:
                if new_quantity > 0:
                    db[product_id]['quantity'] = new_quantity
                else:
                    del db[product_id]  # Remove item if quantity is 0
            else:
                return jsonify({"error": "Product not in cart"}), 404


        return jsonify({"message": "Cart updated"}), 200
    except Exception as e:
        app.logger.error(f"Error in update-quantity: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

#Route for Payment
@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        payment_id = request.form['payment_id']
        order_id = request.form['order_id']
        payment_datetime = request.form['payment_datetime']
        amount = request.form['amount']
        payment_option = request.form['payment_option']
        payment_option_id = request.form['payment_option_id']
        customer_id = request.form['customer_id']


        if payment_option == '1':  # Credit Card
            card_type = request.form['card_type']
            card_number = request.form['card_number']
            expiration_date = request.form['expiration_date']
            security_code = request.form['security_code']
            full_name = request.form['full_name']


            credit_card = PO_CreditCard(payment_option_id, customer_id, card_type, card_number, expiration_date, security_code, full_name)
            payment = Payment(payment_id, order_id, payment_datetime, amount, payment_option, payment_option_id)
           
        elif payment_option == '2':  # Google Pay
            google_account = request.form['google_account']
            google_payment_info = request.form['google_payment_info']


            google_pay = PO_GooglePay(payment_option_id, customer_id, google_account, google_payment_info)
            payment = Payment(payment_id, order_id, payment_datetime, amount, payment_option, payment_option_id)


        elif payment_option == '3':  # PayNow
            paynow_account = request.form['paynow_account']
            paynow_transaction_id = request.form['paynow_transaction_id']


            pay_now = PO_Paynow(payment_option_id, customer_id, paynow_account, paynow_transaction_id)
            payment = Payment(payment_id, order_id, payment_datetime, amount, payment_option, payment_option_id)


        return render_template('payment_success.html', payment=payment)


    return render_template('payment.html')
#Route for payment

@app.route('/history')
def history():
    return render_template('purchasehistory.html')
    
@app.route('/feedback')
def feedbackform():
    return render_template('feedbackform.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/purchase_details')
def purchase_details():
    return render_template('purchase_details')

products = [
    {'id': 1, 'product_name': 'Ultra Facial Toner', 'price': '32', 'stocks': '9000', 'description': 'xxxxxxxx', 'image': 'photo/SkinCare/Toner/UltraFacialToner.jpg', 'points': '40'},
    {'id': 2, 'product_name': 'Sunscreen', 'price': '49', 'stocks': '1200', 'description': 'xxxxxxxx', 'points': '40', 'image' : 'photo/SkinCare/Sunscreen/Sunscreen_Type 1.jpg'},
    {'id': 3, 'product_name': 'Moisturizer', 'price': '18', 'stocks': '9800', 'description': 'xxxxxxxx', 'points': '20', 'image': 'photo/SkinCare/Moisturizer/Moisturizer_Type 1.jpg'},
]

#START OF INVENTORY
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stocks = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    points = db.Column(db.Integer, nullable=True)

@app.route('/inventory')
def inventory():
    products = Product.query.all()
    return render_template('inventory.html', products=products)



@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        # Retrieve form data and add product to the database
        name = request.form['name']
        price = request.form['price']
        stocks = request.form['stocks']
        description = request.form['description']
        points = request.form['points']

        # Add logic to store the product in your database (e.g., SQLAlchemy)
        new_product = Product(name=name, price=price, stocks=stocks, description=description, points=points)
        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for('inventory'))  # Redirect to inventory after adding a product

    return render_template('add_product.html')




# ... (your existing code)

@app.route('/edit_product/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    # Add logic to retrieve and edit the product with the given ID
    product = Product.query.get(id)
    
    if not product:
        flash('Product not found.', 'error')
        return redirect(url_for('inventory'))

    if request.method == 'POST':
        # Update product details based on the form submission
        product.name = request.form['name']
        product.price = request.form['price']
        product.stocks = request.form['stocks']
        product.description = request.form['description']
        product.points = request.form['points']

        # Commit the changes to the database
        db.session.commit()

        flash(f'Product "{product.name}" has been updated successfully.', 'success')
        return redirect(url_for('inventory'))

    # Render the edit_product.html template with the product details
    return render_template('edit_product.html', product=product)

# ... (rest of your code)


# ... (your existing code)

@app.route('/delete_product/<int:id>')
def delete_product(id):
    # Add logic to retrieve and delete the product with the given ID
    product = Product.query.get(id)
    
    if product:
        # Delete the product from the database
        db.session.delete(product)
        db.session.commit()
        flash(f'Product "{product.name}" has been deleted successfully.', 'success')
    else:
        flash('Product not found.', 'error')

    return redirect(url_for('inventory'))

# END OF INVENTORY



# START OF CUSTOMER PROFILE

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contact = db.Column(db.String(15), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

# ... (your existing code)

@app.route('/customerprofile')
def customerprofile():
    customers = Customer.query.all()
    return render_template('customerprofile.html', customers=customers)

@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        # Retrieve form data and add customer to the database
        contact = request.form['contact']
        name = request.form['name']
        email = request.form['email']

        # Add logic to store the customer in your database (e.g., SQLAlchemy)
        new_customer = Customer(contact=contact, name=name, email=email)
        db.session.add(new_customer)
        db.session.commit()

        return redirect(url_for('customerprofile'))  # Redirect to customer profiles after adding a customer

    return render_template('add_customer.html')

@app.route('/edit_customer/<int:id>', methods=['GET', 'POST'])
def edit_customer(id):
    # Add logic to retrieve and edit the customer with the given ID
    customer = Customer.query.get(id)
    
    if not customer:
        flash('Customer not found.', 'error')
        return redirect(url_for('customerprofile'))

    if request.method == 'POST':
        # Update customer details based on the form submission
        customer.contact = request.form['contact']
        customer.name = request.form['name']
        customer.email = request.form['email']

        # Commit the changes to the database
        db.session.commit()

        flash(f'Customer "{customer.name}" has been updated successfully.', 'success')
        return redirect(url_for('customerprofile'))

    # Render the edit_customer.html template with the customer details
    return render_template('edit_customer.html', customer=customer)

@app.route('/delete_customer/<int:id>')
def delete_customer(id):
    customer_to_delete = Customer.query.get(id)
    if customer_to_delete:
        db.session.delete(customer_to_delete)
        db.session.commit()
        flash(f'Customer "{customer_to_delete.name}" has been deleted successfully.', 'success')
    else:
        flash('Customer not found.', 'error')
    return redirect(url_for('customerprofile'))

# END OF CUSTOMER PROFILE



@app.route('/report')
def report():
    # Add your logic for the report route
    return render_template('report.html')

@app.route('/report2')
def report2():
    # Add your logic for the report route
    return render_template('report2.html')


# Classes for payment
class Payment:
    def __init__(self, payment_id, order_id, payment_datetime, amount, payment_option, payment_option_id):
        self.payment_id = payment_id
        self.order_id = order_id
        self.payment_datetime = payment_datetime
        self.amount = amount
        self.payment_option = payment_option
        self.payment_option_id = payment_option_id


class PaymentOption:
    def __init__(self, payment_option_id, customer_id):
        self.payment_option_id = payment_option_id
        self.customer_id = customer_id


class PO_CreditCard(PaymentOption):
    def __init__(self, payment_option_id, customer_id, card_type, card_number, expiration_date, security_code, full_name):
        super().__init__(payment_option_id, customer_id)
        self.card_type = card_type
        self.card_number = card_number
        self.expiration_date = expiration_date
        self.security_code = security_code
        self.full_name = full_name


class PO_GooglePay(PaymentOption):
    def __init__(self, payment_option_id, customer_id, google_account, google_payment_info):
        super().__init__(payment_option_id, customer_id)
        self.google_account = google_account
        self.google_payment_info = google_payment_info


class PO_Paynow(PaymentOption):
    def __init__(self, payment_option_id, customer_id, paynow_account, paynow_transaction_id):
        super().__init__(payment_option_id, customer_id)
        self.paynow_account = paynow_account
        self.paynow_transaction_id = paynow_transaction_id
#classes for payment ^^^

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)