from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from book.models import Category
from order.models import ShopCartForm, ShopCart


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
    if request.method == 'POST': #ürün detay sayfasından post edildiyse
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control==1: #ürün varsa güncelle
                data=ShopCart.objects.get(book_id=id)
                data.quantity += form.cleaned_data['quantity']
                data.save()
            else:#ürün yoksa ekle
                data = ShopCart()  # model ile baglantı
                data.user_id=current_user.id
                data.book_id=id
                data.quantity = form.cleaned_data['quantity']
                data.save()  # veritabanına kaydet
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
        messages.success(request, "Ürün basari ile sepete eklenmiştir.Teşekkür Ederiz")
        return HttpResponseRedirect(url)

    messages.warning(request,"Ürün sepete eklemede hata oluştu.Lütfen tekrar kontrol ediniz.")
    return HttpResponseRedirect(url)



@login_required(login_url='/login')
def shopcart(request):
    category=Category.objects.all()
    current_user =request.user
    schopcart=ShopCart.objects.filter(user_id=current_user.id)
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
    messages.success(request,"Ürün sepetten silinmiştir.")
    return HttpResponseRedirect("/shopcart")
