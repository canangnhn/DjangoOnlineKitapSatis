from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.forms import ModelForm

from book.models import Book


class ShopCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField()

    def __str__(self):
        return self.book

    def __str__(self):
        return self.book.title

    @property
    def amount(self):
        return (self.quantity * self.book.price)

    @property
    def price(self):
        return (self.book.price)



class ShopCartForm(ModelForm):
    class Meta:
        model=ShopCart
        fields =['quantity']

