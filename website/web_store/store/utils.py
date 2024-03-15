import json
from . models import *
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import random
from .decorators import cookie_required
import requests
from django.http import JsonResponse
from django.utils.translation import get_language, gettext_lazy as _
from django.utils.html import strip_tags


def cookie_cart(request):
    if request.COOKIES.get('cookieConsent') != 'true':

        return {'cart_items': 0,'order': None,'items': [], 'total_weight': 0,}
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
                cart = {}
        items = []
        order = {
            'get_cart_total': 0,
            'get_cart_items': 0,
            'get_cart_weight': 0,
            }        
        cart_items = order['get_cart_items']
        for i in cart:
            try:
                cart_items += cart[i]["quantity"]

                product = Product.objects.get(id=i)
                total = (product.price * cart[i]["quantity"])
                weight = (product.weight * cart[i]["quantity"])
                

                order['get_cart_total'] += total
                order['get_cart_items'] += cart[i]["quantity"]
                order['get_cart_weight'] += weight

                item = {
                    'product':{
                        'id': product.id,
                        'name': product.name,
                        'length': product.length,
                        'price': product.price,
                        'weight': product.weight,
                        'image': product.image,

                    },
                    'quantity': cart[i]["quantity"],
                    'get_total': total
                }
                items.append(item)    
            except:
                pass
        return {'cart_items': cart_items, 'order': order, 'items': items}


def cart_data(request):
    if request.COOKIES.get('cookieConsent') != 'true':

        return {'cart_items': 0,'order': None,'items': [],}
    else:
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, confirmed=False)
            items = order.orderitem_set.all()
            cart_items = order.get_cart_items()

            order.get_cart_weight()
            order = {
                'get_cart_total': order.get_cart_total(),
                'get_cart_items': cart_items,
                'get_cart_weight': order.full_weight,
                'order_id': order.order_id
            }

        else:
            cookie_data = cookie_cart(request)
            cart_items = cookie_data['cart_items']
            order = cookie_data['order']
            items = cookie_data['items']

        return {'cart_items': cart_items, 'order': order, 'items': items}

@cookie_required
def guest_order(request, data):
    first_name = data['form']['first_name']
    last_name = data['form']['last_name']
    email = data['form']['email']
    phone_number = data['form']['phone_number']

    cookie_data = cookie_cart(request)
    items = cookie_data['items']

    customer, created = Customer.objects.get_or_create(
        email=email,
    )
    customer.first_name = first_name
    customer.last_name = last_name
    customer.phone_number = phone_number
    customer.save()

    order = Order.objects.create(
        customer=customer,
        confirmed=False,
    )
    for item in items:
        product = Product.objects.get(id=item['product']['id'])

        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )
    return customer, order

def send_confirmation_mail(request, email, confirmation_code):
    subject = _('Email confirmation.')
    from_email = settings.EMAIL_HOST_USER
    to_email = email
    context = {
        'confirmation_code': confirmation_code,
    }

    user_lang = get_language()
    langs = ['en','pl']
    
    if user_lang in langs:
        if user_lang == 'pl':
            email_html_content = render_to_string('emails/email_confirmation_pl.html', context)
        else:
            email_html_content = render_to_string('emails/email_confirmation.html', context)

    email_text_content = strip_tags(email_html_content)

    msg = EmailMultiAlternatives(subject, email_text_content, from_email, [to_email])
    msg.attach_alternative(email_html_content, "text/html")
    msg.send()

def generate_confirmation_code():
    
    confirmation_code = random.randint(1000,9999)

    return confirmation_code

def send_order_confirmation(request, customer, order):
    orderItems = OrderItem.objects.filter(order=order).all()

    user_lang = get_language()
    langs = ['en','pl']

    subject = _('Order confirmation')
    from_email = settings.EMAIL_HOST_USER
    to_email = customer.email
    context = {
        'customer': customer,
        'order': order,
        'orderItems': orderItems,
    }

    if user_lang in langs:
        if user_lang == 'pl':
            email_html_content = render_to_string('emails/order_confirmation_pl.html', context)
        else:
            email_html_content = render_to_string('emails/order_confirmation.html', context)

    email_text_content = strip_tags(email_html_content)

    msg = EmailMultiAlternatives(subject, email_text_content, from_email, [to_email])
    msg.attach_alternative(email_html_content, "text/html")
    msg.send()

def send_return_confirmation(customer, return_request, order):
    return_items = ReturnItem.objects.filter(return_request=return_request).all()

    subject = _('Return confirmation.')

    user_lang = get_language()
    langs = ['en','pl']

    from_email = settings.EMAIL_HOST_USER
    to_email = customer.email
    context = {
        'customer': customer,
        'order': order,
        'return_items': return_items,
        'return_request': return_request,
    }
    if user_lang in langs:
        if user_lang == 'pl':
            email_html_content = render_to_string('emails/return_confirmation.html', context)
        else:
            email_html_content = render_to_string('emails/return_confirmation_pl.html', context)

    email_html_content = render_to_string('emails/return_confirmation.html', context)
    email_text_content = strip_tags(email_html_content)

    msg = EmailMultiAlternatives(subject, email_text_content, from_email, [to_email])
    msg.attach_alternative(email_html_content, "text/html")
    msg.send()

def get_tpay_oauth_token():
    client_id = settings.CLIENT_ID
    client_secret = settings.CLIENT_SECRET

  
    token_url = 'https://api.tpay.com/oauth/auth'



    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    }

    response = requests.post(token_url, data=payload)
    if response.status_code == 200:
        print('Authorization successful')
        return response.json()['access_token']
    else:
        return None

def create_tpay_transaction(order, customer, data):
    url = "https://api.tpay.com/transactions"  

    language = get_language()

    if language == 'pl':
        order_str = 'Zamówienie'
    else:
        order_str = 'Order'

    access_token = get_tpay_oauth_token()

    shipping_address = ShippingAddress.objects.filter(customer=customer).first()

    customer_name = f"{customer.first_name} {customer.last_name}"

    nip=data['invoice'].get('nip', '')
    if nip in data:
        payload = {
            "amount": int(order.full_price),
            "description": f"{order_str}: {order.order_id}",
            "hiddenDescription": f"{order.order_id}",
            "payer": {
                "email": f"{customer.email}",
                "name": f"{customer_name}",
                "phone": f"{customer.phone_number}",
                "address": f"{shipping_address.address}",
                "code": f"{shipping_address.postal_code}",
                "city": f"{shipping_address.city}",
                "country": f"{shipping_address.country.code}",
                "taxId": f"{shipping_address.country.code}{nip}",
                },
            "lang": f"{language}", 
            "callbacks": { 
                "payerUrls": {
                    "success": "https://test.tpay.com/payment_success",
                    "error": "https://test.tpay.com/payment_error."
                },
            }
        }
    else:
        payload = {
            "amount": int(order.full_price),
            "description": f"{order_str}: {order.order_id}",
            "hiddenDescription": f"{order.order_id}",
            "payer": {
                "email": f"{customer.email}",
                "name": f"{customer_name}",
                "phone": f"{customer.phone_number}",
                "address": f"{shipping_address.address}",
                "code": f"{shipping_address.postal_code}",
                "city": f"{shipping_address.city}",
                "country": f"{shipping_address.country.code}",
            },
            "lang": f"{language}",  
            "callbacks": { 
                "payerUrls": {
                    "success": "https://test.tpay.com/payment_success",
                    "error": "https://test.tpay.com/payment_error."
                },
            }
        }

    print(payload)

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    response = requests.post(url,headers=headers, json=payload)

    data = response.text

    print(data)

    if response.status_code in (200, 201):
        return response
    else:
        return JsonResponse({'status': 'error', 'data': data}, status=response.status_code)

