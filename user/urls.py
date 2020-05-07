from django.urls import path

from user import views

urlpatterns = [
    # ex: /blog/
    path('', views.index, name='index'),
   # path('addcomment/<int:id>', views.addcomment, name='addcomment')





]