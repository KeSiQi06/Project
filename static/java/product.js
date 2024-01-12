let openShopping = document.querySelector('.shopping');
let closeShopping = document.querySelector('.closeShopping');
let list = document.querySelector('.list');
let listCard = document.querySelector('.listCard');
let body = document.querySelector('body');
let total = document.querySelector('.all .total');
let quantity = document.querySelector('.all .quantity');

let products = [
    {
        id: 1,
        name: 'Ultra Facial Toner',
        image: 'photo/SkinCare/Toner/UltraFacialToner.jpg',
        description: 'xxxxxxx',
        price: 25
    },
    {
        id: 2,
        name: 'Sunscreen',
        image: 'photo/SkinCare/Sunscreen/Sunscreen_Type 1.jpg',
        description: 'xxxxxxx',
        price: 30
    },
    {
        id: 3,
        name: 'Moisturizer',
        image: 'photo/SkinCare/Moisturizer/Moisturizer_Type 1.jpg',
        description: 'xxxxxxxx',
        price: 25
    },
];

let listCards = [];

function addToCart(productId) {
    const quantity = 1; // Assuming you add one item at a time
    fetch('/add-to-cart', {
        method: 'POST',
        body: JSON.stringify({ productId: productId, quantity: quantity }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log(data.message);
        reloadCart(); // Reload cart from the server
    })
    .catch(error => console.error('Error:', error));
}

function changeQuantity(productId, newQuantity) {
    fetch('/update-quantity', {
        method: 'POST',
        body: JSON.stringify({ productId: productId, quantity: newQuantity }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
        reloadCart(); // Reload cart from server
    })
    .catch(error => console.error('Error:', error));
}

function reloadCart() {
    fetch('/get-cart')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json(); // Parse the JSON response
    })
    .then(cartItems => {
        listCards = cartItems; // Update listCards with items from server
        updateCartUI(); // Call a function to update the UI
    })
    .catch(error => console.error('Error:', error));
}

function updateCartUI() {
    listCard.innerHTML = '';
    let count = 0;
    let totalPrice = 0;

    listCards.forEach(item => {
        // Calculate the total price and count for all items
        totalPrice += item.price * item.quantity;
        count += item.quantity;

        // Create a new list item for each cart item
        let newDiv = document.createElement('li');
        newDiv.innerHTML = `
            <div><img src="static/${item.image}"/></div>
            <div>${item.name}</div>
            <div>$${(item.price * item.quantity).toLocaleString()}</div>
            <div>
                <button onclick="changeQuantity(${item.id}, ${item.quantity - 1})">-</button>
                <div class="count">${item.quantity}</div>
                <button onclick="changeQuantity(${item.id}, ${item.quantity + 1})">+</button>
            </div>`;
        listCard.appendChild(newDiv);
    });

    // Update the total price and quantity after the loop
    total.innerText = `Total Price: $${totalPrice.toLocaleString()}`;
    quantity.innerText = `Total Items: ${count}`;
}


// Function to initialize the application
function initApp() {
    // Render products list
    products.forEach(product => {
        let newDiv = document.createElement('div');
        newDiv.classList.add('item');
        newDiv.innerHTML = `
            <img src="static/${product.image}">
            <div class="title">${product.name}</div>
            <p class="description">${product.description}</p>
            <div class="price">$${product.price.toLocaleString()}</div>
            <button onclick="addToCart(${product.id})">Add To Cart</button>`;
        list.appendChild(newDiv);
    });

    // Load cart items from the server and update the UI
    reloadCart();
}

// Call initApp() to initialize your application
initApp();
