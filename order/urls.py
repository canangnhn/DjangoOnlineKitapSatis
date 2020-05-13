from django.urls import path

from order import views

urlpatterns = [
    # ex: /blog/
    path('', views.index, name='index'),
    path('addtocart/<int:id>', views.addtocart, name='addtocart'),
    path('deletefromcart/<int:id>', views.deletefromcart, name='deletefromcart'),
    path('orderbook/', views.orderbook, name='orderbook')





]