from django.http import JsonResponse, HttpResponseRedirect, FileResponse
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
import json
from .models import *
from django.utils import timezone, translation
from . utils import *
from .forms import *
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db import transaction
from .decorators import cookie_required
import os
from dotenv import load_dotenv

load_dotenv()

def store(request, category_name=None, subcategory_name=None):
    product_displays = ProductDisplay.objects.select_related('product')
    subcategories = []

    if category_name and category_name != _('All'):
        product_displays = product_displays.filter(product__category=category_name)
        subcategories = SUBCATEGORIES.get(category_name, [])

    if subcategory_name:
        product_displays = product_displays.filter(product__subcategory=subcategory_name)

    data = cart_data(request)  
    cart_items = data['cart_items']

    context = {
        'product_displays': product_displays,
        'cart_items': cart_items,
        'categories': CATEGORIES,
        'subcategories': subcategories,
        'current_category': category_name,
        'current_subcategory': subcategory_name,
    }

    return render(request, 'store/store.html', context)


def product(request, product_name, product_color, product_length, product_subcategory):
    data = cart_data(request)
    cart_items = data['cart_items']

    product = get_object_or_404(Product, name=product_name, color=product_color, length=product_length, subcategory=product_subcategory)
    product_variant = ProductVariant.objects.filter(name=product_name, product__color=product_color, subcategory=product_subcategory).all()

    context = {
        'product_variant': product_variant,
        'product': product,
        'cart_items': cart_items,
        'product_name': product_name,
    }

    return render(request, 'store/product.html', context)

def cart(request):
    data = cart_data(request)

    cart_items = data['cart_items']
    order = data['order']
    items = data['items']

    context = {
        'items': items,
        'order': order,
        'cart_items': cart_items,
}
    return render(request, 'store/cart.html', context)



def checkout(request):
    data = cart_data(request)
    cart_items = data['cart_items']
    order = data['order']
    items = data['items']

    countries = Countries.objects.all()

    if request.user.is_authenticated:
        shipping_addresses = ShippingAddress.objects.filter(customer=request.user.customer)

        context = {
            'items': items,
            'order': order,
            'cart_items': cart_items,
            'shipping_addresses': shipping_addresses,
            'countries': countries
        }
    else:
        context = {
            'items': items,
            'order': order,
            'cart_items': cart_items,
            'countries': countries
        }

    return render(request, 'store/checkout.html', context)

@cookie_required    
def update_item(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        product_id = data['Product_id']
        action = data['Action']

        print('Action:', action)
        print('Product_id:', product_id)

        customer = request.user.customer

        order = Order.objects.filter(customer=customer, confirmed=False).first()

        product = Product.objects.get(id=product_id)

        order_item, item_created = OrderItem.objects.get_or_create(order=order, product=product)

        if action == 'add':
            order_item.quantity += 1
        elif action == 'remove':
            if order_item.quantity > 0:
                order_item.quantity -= 1

        if order_item.quantity <= 0:
            order_item.delete()
        else:
            order_item.save()

        return JsonResponse('Item was updated', safe=False)
    else:
        return JsonResponse({'error': _('Invalid request method')}, status=400)

def get_shipping_prices(request):
    if request.method == 'GET':
        shipping_levels = list(ShippingLevels.objects.values())
        return JsonResponse({'shipping_levels': shipping_levels})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
@cookie_required
@require_POST    
def process_order(request):
    order_date = timezone.now().strftime('%Y-%m-%d')
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer

        if not ShippingAddress.objects.filter(customer=customer).exists():
            country = Countries.objects.filter(name=data['shipping']['country']).first()
            shipping_address, created = ShippingAddress.objects.create(
                customer=customer,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                postal_code=data['shipping']['postalcode'],
                country=country,
            )
        else:
            shipping_address = ShippingAddress.objects.get(customer=customer)
        
        order = Order.objects.filter(
            customer=customer,
            confirmed=False
        ).first()

    else:
        customer, order = guest_order(request, data)

    
    if not ShippingAddress.objects.filter(customer=customer).exists():
        if 'shipping' in data:
            country = Countries.objects.filter(name=data['shipping']['country']).first()
            shipping_address = ShippingAddress.objects.create(
                customer=customer,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                postal_code=data['shipping']['postalcode'],
                country=country,
            )
    else:
        shipping_address = ShippingAddress.objects.get(customer=customer)

    if 'invoice' in data:
        country = Countries.objects.filter(name= data['invoice'].get('invoice_country', '')).first()
        invoice_info = InvoiceInfo.objects.create(
            nip=data['invoice'].get('nip', ''),
            firm=data['invoice'].get('firm', ''),
            address=data['invoice'].get('invoice_address', ''),
            city=data['invoice'].get('invoice_city', ''),
            postal_code=data['invoice'].get('invoice_postalcode', ''),
            country=country,
        )

    total = float(data['total'])
    order.order_date = order_date

    selected_shipping_method = data.get('selected_shipping_method')
    selected_shipping_cost = data.get('selected_shipping_cost')

    if total == float(order.get_cart_total() + selected_shipping_cost):
        order.full_price = order.get_cart_total() + selected_shipping_cost
        order.shipping_address = shipping_address
        order.delivery_method = selected_shipping_method
        order.shipping_cost = selected_shipping_cost
        order.save()
        tpay_transaction_response = create_tpay_transaction(order, customer,data)

        if tpay_transaction_response.status_code in [200, 201]:
            response_data = tpay_transaction_response.json()
            transaction_url = response_data['transactionPaymentUrl']
            if transaction_url:
                order.transaction_id = response_data['transactionId']
                order.confirmed = True
                order.save()
                send_order_confirmation(request,customer,order)
                
                return  JsonResponse({'message': 'Payment succesfull...', 'url': transaction_url}, status=200)
            else:
                return JsonResponse({'error': 'Transaction URL not found in the response'}, status=400)
        else:
            return JsonResponse({'message': 'Payment failed'})
    else:
        return JsonResponse({'error': 'Total mismatch'}, status=400)


@cookie_required    
def custom_register(request):
    data = cart_data(request)
    cart_items = data['cart_items']
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            password = form.cleaned_data['password1']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']

            if User.objects.filter(email=email).exists():
                messages.error(request, "Email address already in use.")
            else:    
                confirmation_code = generate_confirmation_code()
                request.session['confirmation_code'] = confirmation_code
                request.session['email'] = email
                request.session['password1'] = password
                request.session['first_name'] = first_name
                request.session['last_name'] = last_name
                request.session['phone_number'] = phone_number
                send_confirmation_mail(request, email, confirmation_code)

                return redirect('confirm_email')
                

    else:
        form = RegisterForm()

    context = {
        'form': form,
        'cart_items': cart_items
    }

    return render(request, 'store/register.html', context)

@cookie_required    
def confirm_email(request):
    data = cart_data(request)
    cart_items = data['cart_items']

    if request.method == 'POST':
        entered_code = request.POST.get('code')
        stored_code = request.session.get('confirmation_code')
        email = request.session.get('email')  
        password = request.session.get('password1')
        first_name=request.session.get('first_name')
        last_name=request.session.get('last_name')
        phone_number=request.session.get('phone_number')

        if int(entered_code) == int(stored_code):
            user = User.objects.create_user(username=email, email=email, password=password,first_name=first_name, last_name=last_name)
            user.save()

            existing_customer = Customer.objects.filter(email=email).first()

            if existing_customer:
                existing_customer.user = user
                existing_customer.first_name = first_name
                existing_customer.last_name = last_name
                existing_customer.email_confirmed = True
                existing_customer.phone_number = phone_number
                existing_customer.save()
            else:
                customer = Customer.objects.create(
                    user=user,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    email_confirmed=True,
                    phone_number=phone_number,
                )
                customer.save()


            login(request, user)

            request.session.pop('confirmation_code', None)
            request.session.pop('email', None)
            request.session.pop('password1', None)
            request.session.pop('first_name', None)
            request.session.pop('last_name', None)
            request.session.pop('phone_number', None)

            return redirect('/')
        else:
            messages.error(request, "Invalid confirmation code. Please try again.")

    context=  {
        'cart_items': cart_items,
    }

    return render(request, 'store/confirm_email.html',context)

@cookie_required    
def custom_login(request):
    data = cart_data(request)

    cart_items = data['cart_items']
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, _("Invalid login credentials."))
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        form = LoginForm()
    context = {
        'form': form,
        'cart_items': cart_items,
        }
    return render(request, 'store/login.html', context)

@cookie_required    
@csrf_exempt
def delete_account(request):
    if request.method == 'DELETE':
        user = request.user
        customer = request.user.customer

        try:
            with transaction.atomic():
                for address in ShippingAddress.objects.filter(customer=customer):
                    for invoice_info in InvoiceInfo.objects.filter(address=address):
                        invoice_info.delete()
                    address.delete()

                for order in Order.objects.filter(customer=customer, complete=True):
                    for order_item in OrderItem.objects.filter(order=order):
                        order_item.delete()
                    order.delete()

                customer.delete()
                user.delete()

            messages.success(request, "Your account has been successfully deleted.")
            response = JsonResponse({'success': True, 'message': "Your account has been successfully deleted."})
        except Exception as e:
            messages.error(request, f"Error deleting your account: {str(e)}")
            response = JsonResponse({'success': False, 'message': "An error occurred while deleting your account."})

        return response

@cookie_required    
def account_delete_confirm(request):
    data = cart_data(request)
    cart_items = data['cart_items']

    context = {
        'cart_items': cart_items,
    }
    return render(request, 'store/account_delete_confirm.html', context)

def set_language(request, language_code):
    supported_languages = ['en', 'pl']

    if language_code in supported_languages:
        translation.activate(language_code)
        request.session['django_language'] = language_code

        response = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        response.set_cookie('django_language', language_code, max_age=365 * 24 * 60 * 60) 
        return response
    else:
        print('failed')


def catalog(request):
    catalog_items = Catalog.objects.all()
    data = cart_data(request)

    cart_items = data['cart_items']

    context = {
        'catalog_items': catalog_items,
        'cart_items': cart_items,
    }
    
    return render(request, 'store/catalog.html', context)

def about_us(request):
    data = cart_data(request)
    cart_items = data['cart_items']

    api_key = settings.GOOGLE_API_KEY

    context = {
        'api_key': api_key,
        'cart_items': cart_items,
    }

    return render(request, 'store/about-us.html',context)

@cookie_required    
def user_profile(request):
    data = cart_data(request)
    cart_items = data['cart_items']

    context = {
        'cart_items': cart_items,
    }

    return render(request, 'store/user_profile.html',context)

@cookie_required    
def user_profile_orders(request):

    customer = request.user.customer
    confirmed_orders = Order.objects.filter(customer=customer, confirmed=True).all()
    completed_orders = Order.objects.filter(customer=customer, complete=True).all()

    data = cart_data(request)

    cart_items = data['cart_items']

    context = {
        'confirmed_orders': confirmed_orders,
        'completed_orders': completed_orders,
        'cart_items': cart_items,
    }

    return render(request, 'store/user_profile_orders.html', context)

@cookie_required    
def user_profile_order_page(request, order_id):

    order = get_object_or_404(Order, order_id=order_id)
    order_items = OrderItem.objects.filter(order=order)

    data = cart_data(request)

    cart_items = data['cart_items']

    context = {
        'order': order,
        'order_items': order_items,
        'cart_items': cart_items,
    }

    return render(request, 'store/user_profile_order_page.html', context)

@cookie_required    
def user_profile_login_data(request):
    user = request.user.customer
    data = cart_data(request)

    cart_items = data['cart_items']

    context = {
        'user': user,
        'cart_items': cart_items,
    }


    return render(request, 'store/user_profile_login_data.html', context)

@cookie_required    
def user_profile_addresses(request):
    customer = request.user.customer
    addresses = ShippingAddress.objects.filter(customer=customer)
    countries = Countries.objects.all()
    data = cart_data(request)

    cart_items = data['cart_items']

    context = {
        'customer': customer,
        'addresses': addresses,
        'cart_items': cart_items,
        'countries': countries,
            }

    return render(request, 'store/user_profile_addresses.html', context)

@cookie_required    
def save_shipping_address(request):
    if request.method == 'POST':
        customer = request.user.customer
        address = request.POST.get('address')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')
        country_code = request.POST.get('country')

        country = get_object_or_404(Countries, code=country_code)

        if ShippingAddress.objects.filter(customer=customer).exists():
            messages.error(request, 'Shipping address already exists')
        else:
            shipping_address = ShippingAddress.objects.create(
                customer=customer, 
                address=address, 
                city=city, 
                postal_code=postal_code, 
                country=country
            )
            shipping_address.save()

            messages.success(request, 'Shipping address saved successfully!')
        return redirect('user_profile_addresses')
    else:
        messages.error(request, 'Invalid request method.')
        return redirect('user_profile_addresses')


def terms_of_service(request):
    data = cart_data(request)
    cart_items = data['cart_items']

    context ={
        'cart_items': cart_items
    }

    return render(request, 'store/terms_of_service.html', context)


def terms_of_service_pdf(request):
    filepath = os.getenv('TERMS_OF_SERVICE_PDF_PATH', 'default/path/to/terms_of_service.pdf')

    with open(filepath, 'rb') as pdf:
            return FileResponse(pdf, as_attachment=True, content_type='application/pdf')

def return_request(request):
    data = cart_data(request)
    cart_items = data['cart_items']

    context ={
        'cart_items': cart_items
    }

    return render(request, 'store/return.html', context)

def fetch_order_items(request):
    data = json.loads(request.body)
    email = data['email']
    order_id = data['order_id']

    try:
        order = Order.objects.get(order_id=order_id, customer__email=email)
        items = OrderItem.objects.filter(order=order)
        item_data = [{'id': item.product.id, 'orderItem_id': item.id, 'name': item.product.name, 'color': item.product.color, 'length': item.product.length, 'quantity': item.quantity} for item in items]
        return JsonResponse({'items': item_data})
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)
 
def return_details(request):
    data = cart_data(request)
    cart_items = data['cart_items']
    item_ids = request.GET.getlist('items[]') 
    order_item_ids = request.GET.getlist('orderItemIds[]')
    order_id = request.GET.get('order_id', None)
    email = request.GET.get('email', None)

    if request.user.is_authenticated:
        customer = request.user.customer
    else:
        customer = Customer.objects.get(email=email)

    order = Order.objects.get(order_id=order_id, customer=customer)

    products = []
    order_items = []

    return_request = ReturnRequest.objects.create(customer=customer, order=order)
    return_request.save()

    if item_ids and order_id:
        for id in item_ids:
            try:
                product = Product.objects.get(id=id)
                products.append(product)
            except Product.DoesNotExist:
                pass
        for id in order_item_ids:
            try:
                order_item = OrderItem.objects.get(id=id)
                order_items.append(order_item)
            except OrderItem.DoesNotExist:
                pass
        context = {
            'products': products,
            'order_items': order_items,
            'order_id': order_id,
            'email': email,
            'cart_items': cart_items  
        }
        return render(request, 'store/return_details.html', context)
    else:
        return redirect('return_page')
    
@require_POST
def process_return(request):
    email = request.POST.get('email')
    order_id = request.POST.get('order_id')

    if request.user.is_authenticated:
        customer = request.user.customer
    else:
        customer = Customer.objects.get(email=email)

    order = Order.objects.get(order_id=order_id)
    return_request = ReturnRequest.objects.get(order=order)
    return_items = json.loads(request.POST.get('returnItems'))

    for product_id, item_details in return_items.items():
        quantity = int(item_details['quantity'])

        product = Product.objects.get(id=product_id)

        ReturnItem.objects.create(
            return_request=return_request,
            product=product,
            quantity=quantity,
        )

    return_request.value = return_request.get_total_value()
    return_request.reason = request.POST.get('reason')
    return_request.bank_account = request.POST.get('bankAccountNumber')
    return_request.confirmed = True
    return_request.save()
    send_return_confirmation(customer, return_request, order)

    return JsonResponse({'message': 'Return request processed successfully', 'redirect': '/store/'})

