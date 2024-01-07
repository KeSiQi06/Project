from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

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
def inventory()
    return render_template('inventory.html')

@app.route('/customerprofile')
def customerprofile()
    return render_template('customerprofile.html')

if __name__ == '__main__':
    app.run(debug=True)

