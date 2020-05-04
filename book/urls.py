from django.urls import path

from . import views

urlpatterns = [
    # ex: /blog/
    path('', views.index, name='index'),
    path('addcomment/<int:id>', views.addcomment, name='addcomment')



]