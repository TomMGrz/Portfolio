from django.db import models
from django.contrib.auth.models import User
from django.core.validators import DecimalValidator
from django.utils.translation import gettext_lazy as _,get_language
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import random
from django_cryptography.fields import encrypt



class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    email_confirmed = models.BooleanField(default=False, null=True, blank=False)
    phone_number = models.CharField(max_length=12, null=True, blank=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}, {self.email}"
    
class Image(models.Model):
    image = models.ImageField(upload_to='images/')

class ProductVariant(models.Model):
    name = models.CharField(max_length=100, null=False, default='None')
    length = models.DecimalField(max_digits = 5, decimal_places = 0, blank=True, null=True)
    subcategory = models.CharField(max_length=100, blank=True, null=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.name}, {self.length}, {self.product.color}"
    
class ProductDisplay(models.Model):
    name = models.CharField(max_length=100, null=True, default='None')
    color = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(Image, null=True, blank=True)
    material = models.CharField(max_length=100, blank=True, null=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    subcategory = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.name}, {self.color}"

STATUS = (
    ("Available", _("Product in stock")),
    ("Unavailable", _("Product not in stock")),
)


CATEGORIES = (
    ("All", _("All")),
    ("Ropes", _("Ropes")),
    ("Strings", _("Strings")),
    ("Mansory Lines", _("Mansory Lines")),
)

SUBCATEGORIES = {
    "Ropes": [_('Polypropylene'), _('Yute')],
    "Strings": [_('Cotton'), _('Synthetic'), _('Plastic')],
    "Mansory Lines": [_('Braided'), _('Twisted')]
}
class Product(models.Model):
    name = models.CharField(max_length=100, null=True)
    diameter = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    length = models.DecimalField(max_digits = 5, decimal_places = 0, blank=True, null=True)
    material = models.CharField(max_length=100, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    weight_per_meter = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    description = models.CharField(max_length=400, null=True, blank = True)
    status = models.CharField(max_length=100,choices=STATUS, default='Available' )
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, validators=[DecimalValidator(8, 2)])
    image = models.ImageField(Image, null=True, blank=True)
    price_per_meter = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    category = models.CharField(max_length=100, choices=CATEGORIES, default=None, null=True, blank = True)
    subcategory = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.price_per_meter is not None:
            self.price = self.price_per_meter * self.length

        if self.weight_per_meter is not None:
            self.weight = self.weight_per_meter * self.length    

        super(Product, self).save(*args, **kwargs)


        if self.status == 'Available':
            if not ProductDisplay.objects.filter(name=self.name, color=self.color,subcategory=self.subcategory).exists():
                product_display = ProductDisplay(name=self.name, color=self.color, product=self, material=self.material, subcategory=self.subcategory)
                product_display.save()
     
        if not ProductVariant.objects.filter(product=self, length=self.length, subcategory=self.subcategory ).exists():
            variant = ProductVariant(name=self.name, length=self.length,subcategory=self.subcategory, product=self)
            variant.save()

    def get_subcategories(self):
        return SUBCATEGORIES.get(self.category, [])

    def __str__(self):
        return f"#{self.id} {self.name}, {self.length}, {self.color}, {self.subcategory}"

class Catalog(models.Model):
    name = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=500,  null=True, blank=True)
    image = models.ImageField(Image, null=True, blank=True)
    image2 = models.ImageField(Image, null=True, blank=True)
    image3 = models.ImageField(Image, null=True, blank=True)
    image4 = models.ImageField(Image, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'

SHIPPING_STATUS = [
        ('Pending', _('Pending')),
        ('Shipped', _('Shipped')),
        ('Delivered', _('Delivered')),
        ('Cancelled', _('Cancelled')),
    ]

class Order(models.Model):
    order_id = models.CharField(max_length=6, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank = True)
    shipping_address = models.ForeignKey("ShippingAddress", on_delete=models.SET_NULL, null = True, blank = True)
    order_date = models.DateField(auto_now_add=True)
    transaction_id = models.CharField(max_length = 20, null = True, blank=True)
    full_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    full_weight = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    confirmed = models.BooleanField(default=False, null=True, blank=False)
    shipping_number = models.CharField(max_length=20, null=True, blank=True)
    delivery_method = models.CharField(max_length=100, null=True, blank=True)
    shipping_status = models.CharField(max_length=20, choices=SHIPPING_STATUS, default='Pending',null=True, blank=True)
    shipping_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    complete = models.BooleanField(default=False, null=True, blank=False)
    invoice = models.FileField(upload_to='order_invoices/', blank=True, null=True)

    ### dodać automatyczne wysłanie fakury jeśli shipping status = Delivered, zmienić wtedy status na complete
    ## dodać powiadomienie o wysłanie faktury

    def __str__(self):
        return 'Order #' f'{self.id}, {self.customer}, {self.order_date}, {self.confirmed}'
    
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total() for item in orderitems])
        self.full_price = total
        self.save()
        return total
    
    def get_cart_weight(self):
        orderitems = self.orderitem_set.all()
        total_weight = sum([item.product.weight * item.quantity for item in orderitems])
        self.full_weight = total_weight
        return total_weight

    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
    
    def generate_order_id(self):
        if not self.order_id:
            while True:
                order_id = str(random.randint(100000, 999999))
                if not Order.objects.filter(order_id=order_id).exists():
                    self.order_id = order_id
                    break

    def confirm_order(self):
        if self.invoice and self.shipping_status == 'Delivered':
            self.complete = True
            self.send_invoice_email()
            print('Email sent successfully')
        else:
            pass

    def send_invoice_email(self):
        subject = 'Invoice for Your Order'
        from_email = settings.EMAIL_HOST_USER
        to_email = self.customer.email

        customer_name = self.customer.first_name + ' ' + self.customer.last_name
        order_id = self.order_id

        
        user_lang = get_language()
        langs = ['en','pl']

        context = {
            'customer_name': customer_name,
            'order_id': order_id,
        }

        if user_lang in langs:
            if user_lang == 'pl':
                email_html_content = render_to_string('emails/invoice_pl.html', context)
            else:
                email_html_content = render_to_string('emails/invoice.html', context)
        email_text_content = strip_tags(email_html_content)

        msg = EmailMultiAlternatives(subject, email_text_content, from_email, to_email)
        msg.attach_alternative(email_html_content, "text/html")

        if self.invoice:
            msg.attach(self.invoice.name, self.invoice.read(), self.invoice.file.content_type)


        msg.send()

    def save(self, *args, **kwargs):
        self.generate_order_id() 
        self.confirm_order()
        super(Order, self).save(*args, **kwargs)
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    adding_date = models.DateField(auto_now_add=True)

    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
    def get_total_weight(self):
        total = self.product.weight * self.quantity
        return total
    
    def __str__(self):
        return 'Item #' f'{self.id}, Order: {self.order.order_id} ' 'Product: ' f'{self.product} x{self.quantity},' 

class Countries(models.Model):
    name = models.CharField(max_length = 100, null=True, blank = True)
    code = models.CharField(max_length =2, null=True, blank = True)
    def __str__(self):
        return f'{self.name}, {self.code}' 

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    city = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    postal_code = models.CharField(max_length=200, null=True)
    country = models.ForeignKey(Countries, on_delete=models.SET_NULL, null=True, blank=True)
    adding_date = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.customer}'

class InvoiceInfo(models.Model):
    nip = models.CharField(max_length=10, blank=True, null=True)
    firm = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    postal_code = models.CharField(max_length=200, null=True)
    country = models.ForeignKey(Countries, on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return f'{self.firm}, {self.nip}, {self.address}'
    

class ShippingLevels(models.Model):
    min_weight = models.DecimalField(max_digits=5, decimal_places=2) 
    max_weight = models.DecimalField(max_digits=5, decimal_places=2)  
    cost = models.DecimalField(max_digits=8, decimal_places=2)
    courier_name = models.CharField(max_length=100, blank=False, null=False) 

    def __str__(self):
        return f"{self.courier_name}, {self.min_weight}kg - {self.max_weight}kg: {self.cost} pln"
    
    @staticmethod
    def calculate_shipping_cost(weight, courier_name):
        try:
            shipping_level = ShippingLevels.objects.get(
                courier_name=courier_name, 
                min_weight__lte=weight, 
                max_weight__gte=weight
            )
            return shipping_level.cost
        except ShippingLevels.DoesNotExist:
            return None
        except ShippingLevels.MultipleObjectsReturned:
            return ShippingLevels.objects.filter(
                courier_name=courier_name, 
                min_weight__lte=weight, 
                max_weight__gte=weight
            ).first().cost
        
class Currencies(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=20)
    symbol = models.CharField(max_length=10)
    conversion_rate = models.DecimalField(max_digits=10, decimal_places=6)
    is_base = models.BooleanField(default=False)

    def __str__(self):
        return self.name, self.code
    
    def save(self, *args, **kwargs):
        self.code = self.code.upper()
        super().save(*args, **kwargs)

RETURN_STATUS= [
    ('Pending', _('Pending')),
    ('Approved', _('Approved')),
    ('Rejected', _('Rejected')),
]

class ReturnRequest(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    return_id = models.CharField(max_length=6, null=True, blank=True)
    value = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    reason = models.CharField(max_length=500)
    status = models.CharField(max_length=100, choices=RETURN_STATUS, default='Pending')
    adding_date = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False, null=True, blank=False)
    complete = models.BooleanField(default=False, null=True, blank=False)
    bank_account = encrypt(models.CharField(max_length=100))
    def __str__(self):
        return f"{self.return_id},order{self.order.order_id}, {self.customer}"

    def generate_return_id(self):
        if not self.return_id:
            while True:
                return_id = str(random.randint(100000, 999999))
                if not ReturnRequest.objects.filter(return_id=return_id).exists():
                    self.return_id = return_id
                    break

    def get_total_value(self):
        returnitems = self.return_items.all()
        total = sum([item.get_total() for item in returnitems])
        self.value = total
        self.save()
        return total
    
    def save(self, *args, **kwargs):
        self.generate_return_id()
        super(ReturnRequest, self).save(*args, **kwargs)

    
class ReturnItem(models.Model):
    return_request = models.ForeignKey(ReturnRequest, on_delete=models.SET_NULL, null=True, blank=True, related_name='return_items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)

    def get_total(self):
        total = self.product.price * self.quantity
        return total

    def __str__(self):
        return f'{self.return_request.id}, {self.product}, {self.quantity}'