from flask import Flask, render_template, url_for, request, session, redirect
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


@app.route('/login', methods=['GET', 'POST'])  # Add this decorator if it's missing
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/purchase_details')
def purchase_details():
    return render_template('purchase_details')

@app.route('/inventory')
def inventory():
    return render_template('inventory.html')

@app.route('/customerprofile')
def customerprofile():
    return render_template('customerprofile.html')

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
