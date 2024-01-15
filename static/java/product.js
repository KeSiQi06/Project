let openShopping = document.querySelector('.shopping');
let closeShopping = document.querySelector('.closeShopping');
let list = document.querySelector('.list');
let listCard = document.querySelector('.listCard');
let body = document.querySelector('body');
let total = document.querySelector('.all .total');
let quantity = document.querySelector('.all .quantity');


document.body.addEventListener('click', function(event) {
    if (event.target.matches("button.add-to-cart")) {
        const productId = parseInt(event.target.dataset.productId, 10);
        addToCart(productId);
    } else if (event.target.matches(".increase-quantity") || event.target.matches(".decrease-quantity")) {
        const productId = parseInt(event.target.dataset.productId, 10);
        const action = event.target.matches(".increase-quantity") ? 'increase' : 'decrease';
        changeQuantity(productId, action);
    }
});


let products = [
    {
        id: 1,
        name: 'Ultra Facial Toner',
        image: 'photo/SkinCare/Toner/UltraFacialToner.jpg',
        description: 'xxxxxxx',
        price: 32
    },
    {
        id: 2,
        name: 'Sunscreen',
        image: 'photo/SkinCare/Sunscreen/Sunscreen_Type 1.jpg',
        description: 'xxxxxxx',
        price: 49
    },
    {
        id: 3,
        name: 'Moisturizer',
        image: 'photo/SkinCare/Moisturizer/Moisturizer_Type 1.jpg',
        description: 'xxxxxxxx',
        price: 18
    },
];


let listCards = [];


function addToCart(productId) {
    const existingItem = listCards.find(item => item.productId === productId);
    const quantity = existingItem ? existingItem.quantity + 1 : 1;


    // Find the product with the given productId in your product list
    const product = products.find(p => p.id === productId);


    if (product) {
        // Include the 'image' property in the JSON data
        const requestData = {
            productId: productId,
            quantity: quantity,
            image: product.image, // Include the product's image URL
        };


        fetch('/add-to-cart', {
            method: 'POST',
            body: JSON.stringify(requestData),
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
    } else {
        console.error('Product not found in the product list');
    }
}


function changeQuantity(productId, action) {
    const cartItem = listCards.find(item => item.product_id == productId);
    if (!cartItem) {
        console.error('Product not found in cart');
        return;
    }


    let newQuantity = action === 'increase' ? cartItem.quantity + 1 : cartItem.quantity - 1;
    if (newQuantity < 0) newQuantity = 0;


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
        reloadCart();
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
    listCard = document.querySelector('.listCard'); // Find the listCard element


    if (listCard) {
        listCard.innerHTML = '';
        let count = 0;
        let totalPrice = 0;


        listCards.forEach(item => {
            let totalPriceItem = parseFloat(item.price) * item.quantity;
            totalPrice += totalPriceItem;
            count += item.quantity;
   
            let newDiv = document.createElement('li');
            newDiv.innerHTML = `
                <div><img src="/static/${item.image}" alt="${item.name}" /></div>
                <div>${item.name}</div>
                <div>$${totalPriceItem.toFixed(2)}</div>
                <div>
                    <button class="decrease-quantity" data-product-id="${item.product_id}">-</button>
                    <div class="count">${item.quantity}</div>
                    <button class="increase-quantity" data-product-id="${item.product_id}">+</button>
                </div>`;
            listCard.appendChild(newDiv);
        });


        total.innerText = `Total Price: $${totalPrice.toFixed(2)}`;
        quantity.innerText = `Total Items: ${count}`;
    }
}


// Function to initialize the application
function initApp() {
    // Render products list
       // existing code to render products...
       products.forEach(product => {
        let newDiv = document.createElement('div');
        newDiv.classList.add('item');
        newDiv.innerHTML = `
        <img src="/static/${product.image}">
        <div class="title">${product.name}</div>
        <p class="description">${product.description}</p>
        <div class="price">$${product.price.toLocaleString()}</div>
        <button class="add-to-cart" data-product-id="${product.id}">Add To Cart</button>`;
        list.appendChild(newDiv);
    });


    reloadCart();
}


// Call initApp() to initialize your application
initApp();

