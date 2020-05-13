from django.contrib import admin

# Register your models here.
from order.models import ShopCart, OrderBook, Order


class ShopCartAdmin(admin.ModelAdmin):
    list_display = ['user','book','price','quantity','amount']
    list_filter = ['user']


class OrderBookline(admin.TabularInline):
    model =OrderBook
    readonly_fields = ('user','book','price','quantity','amount')
    can_delete = False
    extra = 0



class OrderAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'city', 'total','status']
    list_filter = ['status']
    readonly_fields = ['user','address','city','country', 'phone','first_name','ip','last_name','phone', 'city', 'total']
    inlines = [OrderBookline]
    can_delete=False

class OrderBookAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'price', 'quantity', 'amount']
    list_filter = ['user']

admin.site.register(ShopCart,ShopCartAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderBook,OrderBookAdmin)