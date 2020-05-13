from unicodedata import category

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.utils.crypto import get_random_string

from book.models import Category, Book
from home.models import UserProfile
from order.models import ShopCartForm, ShopCart, OrderForm, Order, OrderBook


def index(request):
    text="Merhaba Django";

    return HttpResponse("Order App")

@login_required(login_url='/login') #check login
def addtocart(request,id):
    url = request.META.get('HTTP_REFERER')
    current_user=request.user
    checkbook=ShopCart.objects.filter(book_id=id)
    if checkbook:
        control=1 #ürün sepette var
    else:
        control=0 #ürün sepette yok
    if request.method == 'POST':  # Form post edildiyse, ürün detay sayfasından geldiyse
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control == 1:  # ürün varsa güncelle
                data = ShopCart.objects.get(book_id=id)  # get 1 eleman çağırır,filtre liste cağırır
                data.quantity += form.cleaned_data['quantity']
                data.save()  # ver,tabanına kaydet
            else:  # ürün yoksa ekle
                data = ShopCart()  # model ile bağlantı kur
                data.user_id = current_user.id
                data.book_id = id
                data.quantity = form.cleaned_data['quantity']
                data.save()  # veritabanına kaydet
            request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
            messages.success(request, "Ürün basari ile sepete eklenmiştir.Teşekkür Ederiz")
            return HttpResponseRedirect(url)

    else: #ürün direk sepette ekle butonuna basıldıysa
        if control == 1:  # ürün varsa güncelle
            data = ShopCart.objects.get(book_id=id)
            data.quantity += 1
            data.save()
        else:  # ürün yoksa ekle
            data=ShopCart()
            data.user_id=current_user.id
            data.book_id=id
            data.quantity =1
            data.save()
        request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
        messages.success(request, "Ürün basari ile sepete eklenmiştir.Teşekkür Ederiz")
        return HttpResponseRedirect(url)

    messages.warning(request,form.errors)
    return HttpResponseRedirect(url)



@login_required(login_url='/login')
def shopcart(request):
    category=Category.objects.all()
    current_user =request.user
    schopcart=ShopCart.objects.filter(user_id=current_user.id)
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()

    total=0
    for rs in schopcart:
        total += rs.book.price * rs.quantity

    context={ 'schopcart':schopcart,
              'category':category,
              'total':total,
              }

    return render(request, 'Shopcart_book.html',context)


@login_required(login_url='/login')
def deletefromcart(request,id):
    ShopCart.objects.filter(id=id).delete()
    current_user=request.user
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
    messages.success(request,"Ürün sepetten silinmiştir.")
    return HttpResponseRedirect("/shopcart")


@login_required(login_url='/login')
def orderbook(request):
    category=Category.objects.all()
    current_user=request.user
    schopcart=ShopCart.objects.filter(user_id=current_user.id)
    total=0
    for rs in schopcart:
        total +=rs.book.price * rs.quantity

    if request.method == 'POST':
        form=OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.first_name=form.cleaned_data['first_name']
            data.last_name=form.cleaned_data['last_name']
            data.address=form.cleaned_data['address']
            data.city=form.cleaned_data['city']
            data.phone=form.cleaned_data['phone']
            data.user_id=current_user.id
            data.total=total
            data.ip=request.META.get('REMOTE_ADDR')
            ordercode=get_random_string(5).upper()
            data.code=ordercode
            data.save()

            schopcart = ShopCart.objects.filter(user_id=current_user.id)
            for rs in schopcart:
                detail=OrderBook()
                detail.order_id =data.id #order id
                detail.book_id=rs.book_id
                detail.user_id=current_user.id
                detail.quantity=rs.quantity


                book=Book.objects.get(id=rs.book_id)
                book.amount -=rs.quantity
                book.save()

                detail.price     =rs.book.price
                detail.amount    =rs.amount
                detail.save()

            ShopCart.objects.filter(user_id=current_user.id).delete()
            request.session['cart_items']=0
            messages.success(request,"Your Order has been completed.Thank you")
            return render(request,'Order_Completed.html',{'ordercode':ordercode,'category':category})
        else:
            messages.warning(request,form.errors)
            return HttpResponseRedirect("/order/orderbook")

    form=OrderForm()
    profile=UserProfile.objects.get(user_id=current_user.id)
    context={
        'schopcart':shopcart,
        'category':category,
        'total':total,
        'form':form,
        'profile':profile,
    }
    return render(request,'Order_Form.html',context)