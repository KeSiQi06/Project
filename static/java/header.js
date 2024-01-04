document.addEventListener('DOMContentLoaded', function () {
    let openShopping = document.querySelector('.shopping');
    let closeShopping = document.querySelector('.closeShopping');
    let list = document.querySelector('.list');
    let listCard = document.querySelector('.listCard');
    let body = document.querySelector('body');
    let total = document.querySelector('.total');
    let quantity = document.querySelector('.quantity');

    openShopping.addEventListener('click', () => {
        body.classList.add('active');
    });

    closeShopping.addEventListener('click', () => {
        body.classList.remove('active');
    });

    // Select the menu and sub-menu elements
    var menu = document.getElementById('menu');
    var subMenu = document.querySelector('.sub-menu');

    // Toggle the sub-menu on click
    menu.addEventListener('click', function () {
        subMenu.style.display = (subMenu.style.display === 'block' ? 'none' : 'block');
    });
});
