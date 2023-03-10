# from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="ShopHome"),
    path('about/', views.about, name="AboutUs"),
    path('contactus/', views.contactus, name="ContactUs"),
    path('tracker/', views.tracker, name="TrackingStatus"),
    path('search/', views.search, name="Search"),
    path('products/<int:pid>', views.products, name="Product"),
    path('checkout/', views.checkout, name="Checkout"),
    path('HandleRequest/', views.HandleRequest, name="HandleRequest"),
]
