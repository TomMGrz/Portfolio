from django.shortcuts import render
from .models import *

def portfolio(request, category_name=None):
    if category_name is None or category_name == "Wszystkie":
        portfolio_objects = Portfolio.objects.all()
    else:
        portfolio_objects = Portfolio.objects.filter(category=category_name)

    categories = [('Wszystkie', 'Wszystkie')] + list(CATEGORIES)
    context = {'portfolio_objects': portfolio_objects, 'categories': categories}
    return render(request, 'site/portfolio.html', context)

def about_me(request):

    about_me_obj = AboutMe.objects.first()

    context = {'about_me_obj': about_me_obj}
    
    return render(request, 'site/about_me.html', context)

def contact(request):

    contact_obj = Contact.objects.first()

    context = {'contact_obj': contact_obj}

    return render(request, 'site/contact.html', context)