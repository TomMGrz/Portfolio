console.log("Cart.js loaded");

var updateBtns = document.getElementsByClassName('update-cart')

for(var i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var product_id = this.dataset.product;
        var action = this.dataset.action;
        console.log('Product_id:',product_id, 'Action:', action);

        console.log('USER: ', user)
        if(user == 'AnonymousUser'){
            addCookieItem(product_id, action)
        }else{
            updateUserOrder(product_id, action)
        }

    })
}

function addCookieItem(product_id, action) {
    console.log('Not logged in..');

    if (action == 'add') {
        if (cart[product_id] === undefined) {
            cart[product_id] = { 'quantity': 1 };
        } else {
            cart[product_id]['quantity'] += 1;
        }
    } else if (action == 'remove') {
        if (cart[product_id] === undefined) {
            cart[product_id] = { 'quantity': 0 };
        }

        cart[product_id]['quantity'] -= 1;

        if (cart[product_id]['quantity'] <= 0) {
            console.log('Remove item');
            delete cart[product_id];
        }
    }

    console.log('Cart: ', cart);
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";
    location.reload();
}

function updateUserOrder(product_id, action) {
    console.log('Logged in, sending data...')

    var url = '/update_item/'

    console.log('Sending JSON data:', JSON.stringify({'Product_id': product_id, 'Action': action}));
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'Product_id': product_id, 'Action': action})
    })

    .then((response) => {
        return response.json()
    })

    .then((data) => {
        console.log('data:', data)
        location.reload()
    })

    .then((data) => {
        console.log('data:', data);
        document.getElementById('cart-count').innerText = data.cart_items;
    });
}