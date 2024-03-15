from django.urls import path
from . import views

urlpatterns =[
    path('', views.about_me, name='about_me'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('portfolio/<str:category_name>/', views.portfolio, name='portfolio_by_category'),
    path('contact/', views.contact, name='contact')
]