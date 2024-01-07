let openShopping = document.querySelector('.shopping');
let closeShopping = document.querySelector('.closeShopping');
let list = document.querySelector('.list');
let listCard = document.querySelector('.listCard');
let body = document.querySelector('body');
let total = document.querySelector('.total');
let quantity = document.querySelector('.quantity');

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

let listCards  = [];

function initApp() {
    products.forEach((value, key) => {
      let newDiv = document.createElement('div');
      newDiv.classList.add('item');
      newDiv.innerHTML = `
        <img src="static/${value.image}">
        <div class="title">${value.name}</div>
        <p class="description">${value.description}</p>
        <div class="price">$${value.price.toLocaleString()}</div>
        <button onclick="addToCard(${key})">Add To Cart</button>`;
      list.appendChild(newDiv);

    });
}
  
  initApp();

  function addToCard(key) {
    if (listCards[key]) {
      // If the item is already in the cart, increase the quantity
      listCards[key].quantity += 1;
    } else {
      // If the item is not in the cart, add it with quantity 1
      listCards[key] = JSON.parse(JSON.stringify(products[key]));
      listCards[key].quantity = 1;
    }
  
    // Store the updated cart in localStorage
    localStorage.setItem('cartItems', JSON.stringify(Object.values(listCards)));
  
    reloadCard();
  }

function reloadCard() {
  listCard.innerHTML = '';
  let count = 0;
  let totalPrice = 0;

  // Loop through the cart items and update the quantity and total price
  listCards.forEach((value, key) => {
    totalPrice += value.price * value.quantity;
    count += value.quantity;

    if (value) {
      let newDiv = document.createElement('li');
      newDiv.innerHTML = `
        <div><img src="static/${value.image}"></div>
        <div>${value.name}</div>
        <div>$${(value.price * value.quantity).toLocaleString()}</div>
        <div>
          <button onclick="changeQuantity(${key}, ${value.quantity - 1})">-</button>
          <div class="count">${value.quantity}</div>
          <button onclick="changeQuantity(${key}, ${value.quantity + 1})">+</button>
        </div>`;
      listCard.appendChild(newDiv);
    }
  });

  total.innerText = `$${totalPrice.toLocaleString()}`;
  quantity.innerText = count;
}

function changeQuantity(key, quantity) {
    if (quantity == 0) {
      delete listCards[key];
    } else {
      listCards[key].quantity = quantity;
    }
    // Store the updated cart in localStorage
    localStorage.setItem('cartItems', JSON.stringify(Object.values(listCards)));
  
    reloadCard();
  }

