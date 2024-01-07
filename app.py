from flask import Flask, render_template, url_for, request, session, redirect

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
                return redirect(url_for('home'))
            else:
                return 'Staff login failed. Please check your credentials.'

        elif user_type == 'member':
            for user in users:
                if user['email'] == email and user['password'] == password:
                    session['user_name'] = user['name']
                    return redirect(url_for('home'))
            return 'Member login failed. Please check your credentials.'

    return render_template('login.html')

@app.route('/staff_login', methods=['GET', 'POST'])
def staff_login():
    if request.method == 'POST':
        staff_id = request.form.get('staff_id')
        password = request.form.get('password')

        # Hardcoded staff credentials
        if staff_id == '2468' and password == 'NYP2024':
            # Assuming you want to redirect to the homepage upon successful login
            # You can set a session variable or a flag to indicate a successful staff login
            session['staff'] = True
            return redirect(url_for('home'))
        else:
            return 'Invalid Staff ID or Password'

    return render_template('staff_login.html')

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

@app.route('/payment')
def payment():
    return render_template('payment.html')

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

if __name__ == '__main__':
    app.run(debug=True)

