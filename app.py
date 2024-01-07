from flask import Flask, render_template, url_for, request, session, redirect

app = Flask(__name__)

# Set a secure secret key (change 'your_secret_key' to a strong, unique key)
app.secret_key = 'your_secret_key'

users = []  # Initialize an empty list to store user data

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        birthday = request.form['birthday']
        
        # Store the user data (in a real application, use a database)
        users.append({'name': name, 'email': email, 'password': password, 'birthday': birthday})
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Check if the email and password match (in a real application, use a database)
        for user in users:
            if user['email'] == email and user['password'] == password:
                session['user_email'] = email  # Store the user's email in the session
                return f'Logged in as {user["name"]}'
        return 'Login failed. Please check your credentials.'
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_email', None)  # Remove the user's email from the session
    return redirect(url_for('index'))



@app.route('/product')
def product():
    return render_template('product.html')

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/payment')
def payment():
    return render_template('payment.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

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

