from flask import Flask, render_template, url_for, request, session, redirect, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

users = []

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
        hashed_password = generate_password_hash(password)
        birthday = request.form['birthday']
        
        # Check if email already exists
        if any(user['email'] == email for user in users):
            return render_template('signup.html', error="Email already registered.")

        # Add the new user to the users list
        users.append({'name': name, 'email': email, 'password': hashed_password, 'birthday': birthday})
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
            user = next((u for u in users if u['email'] == email), None)
            if user and check_password_hash(user['password'], password):
                session['user_name'] = user['name']
                return redirect(url_for('home'))
            else:
                return 'Member login failed. Please check your credentials.'

    return render_template('login.html')

    
@app.route('/logout')
def logout():
    session.pop('user_name', None)
    return redirect(url_for('home'))

@app.route('/product')
def product():
    return render_template('product.html')

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

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/purchase_details')
def purchase_details():
    return render_template('purchase_details')

<<<<<<< HEAD
@app.route('/inventory')
def inventory():
    return render_template('inventory.html')

@app.route('/customerprofile')
def customerprofile():
    return render_template('customerprofile.html')
=======

#inventory
# List to store product data (replace this with a database in a real application)
products = [
    {'id': 1, 'product_name': 'Moisturiser', 'price': '$32', 'stocks': '9000', 'description': 'xxxxxxxx', 'points': '40'},
    {'id': 2, 'product_name': 'Serum', 'price': '$49', 'stocks': '1200', 'description': 'xxxxxxxx', 'points': '40'},
    {'id': 3, 'product_name': 'Lip Balm', 'price': '$18', 'stocks': '9800', 'description': 'xxxxxxxx', 'points': '20'},
]

@app.route('/inventory')
def inventory():
    return render_template('inventory.html', products=products)

@app.route('/add_product', methods=['POST'])
def add_product():
    new_product_data = {
        'id': len(products) + 1,  # Ensure a unique ID for the new product
        'product_name': request.form.get('product_name'),
        'price': request.form.get('price'),
        'stocks': request.form.get('stocks'),
        'description': request.form.get('description'),
        'points': request.form.get('points'),
    }

    products.append(new_product_data)

    return render_template('inventory.html', products=products)

@app.route('/remove_product', methods=['POST'])
def remove_product():
    product_id = int(request.form.get('product_id'))

    # Find the product with the given id and remove it
    for product in products:
        if product['id'] == product_id:
            products.remove(product)
            return jsonify({'status': 'success', 'message': 'Product removed successfully'})

    # If the product with the given ID is not found
    return jsonify({'status': 'error', 'message': 'Product not found'})
#end of inventory

@app.route('/customer_profile')
def customer_profile():
    # Add your logic for the customer profile route
    return render_template('customerprofile.html')

@app.route('/report')
def report():
    # Add your logic for the report route
    return render_template('report.html')

@app.route('/report2')
def report2():
    # Add your logic for the report route
    return render_template('report2.html')



if __name__ == '__main__':
    app.run(debug=True)

#end of customer profile
    
>>>>>>> 048ffcc01d5548468d7f06db256c9c497e1ae5c7

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
    app.run(debug=True)
