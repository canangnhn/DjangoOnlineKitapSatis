import json
from tkinter import Menu
from unicodedata import category

from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
import book
from book.models import Book, Category, Images, Comment
from home.form import SearchForm, SignUpForm
from home.models import Setting, ContactFormMessage, ContactFormu, FAQ
from order.models import ShopCart


def index(request):
    current_user=request.user
    setting=Setting.objects.get(pk=1);
    sliderdata = Book.objects.all()[:1]
    category=Category.objects.all()
    daybooks=Book.objects.all()[:3]
    lastbooks = Book.objects.all().order_by('-id')[:4]
    randombooks = Book.objects.all().order_by('?')[:3]
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()




    context={'setting': setting,
             'category': category,
             'page':'home',
             'sliderdata': sliderdata,
             'daybooks': daybooks,
             'lastbooks': lastbooks,
             'randombooks': randombooks,

             }
    return render(request,'index.html',context)


def hakkimizda(request):
    setting=Setting.objects.get(pk=1);
    context={'setting': setting,
             'category': category,
             'page':hakkimizda}
    return render(request,'hakkimizda.html',context)


def referanslar(request):
    setting=Setting.objects.get(pk=1);
    context={'setting': setting,
             'category': category,
             'page':referanslar}
    return render(request,'referanslarimiz.html',context)


def iletisim(request):
    ###Formu  kaydetmek için
    if request.method =='POST':#post ediliyorsa
        form=ContactFormu(request.POST);
        if form.is_valid() :
            data= ContactFormMessage() #model ile baglantı kur.
            data.name=form.cleaned_data['name'] #formdan bilgi al
            data.email = form.cleaned_data['email']
            data.subject=form.cleaned_data['subject']
            data.message=form.cleaned_data['message']
            data.ip=request.META.get('REMOTE_ADDR')
            data.save()  #veritabanına kaydet
            messages.success(request,"Mesaj başarı ile gönderilmiştir.Teşekkür ederiz.")
            return HttpResponseRedirect('/iletisim')
##Forma ulaşmak için

    setting=Setting.objects.get(pk=1)
    #form=ContactFormu()
    context={'setting': setting,
             'category': category
            # 'form' : form
    }
    return render(request,'iletisim.html',context)




def category_books(request,id,slug):
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    books=Book.objects.filter(category_id=id)
    context={'books': books,
             'category': category,
             'categorydata':categorydata }
    return render(request,'books.html',context)


def book_detail(request,id,slug):
    category= Category.objects.all()
    book=Book.objects.get(pk=id)
    images =Images.objects.filter(book_id=id)
    comments=Comment.objects.filter(book_id=id,status='True')
    context ={'book': book,
              'category':category,
              'images':images,
              'comments':comments,
    }
    return render(request,'book_detail.html',context)


def book_asearch(request):
     return render(request,'asearch.html')


def book_search(request):
    ###Formu  kaydetmek için
    if request.method =='POST':#post ediliyorsa
        form=SearchForm(request.POST);
        if form.is_valid() :
            category=Category.objects.all() #Get form data


            query=form.cleaned_data['query'] #formdan bilgiyi al
            catid= form.cleaned_data['catid'] #Get form data
            #return HttpResponse(catid)
            if catid==0:
                books = Book.objects.filter(title__icontains=query)
            else:
                books = Book.objects.filter(title__icontains=query,category_id=catid)

            context={'books': books,
                    'category':category,
            }
            return render(request,'book_search.html',context)

    return HttpResponseRedirect('/')



def book_search_auto(request):
  if request.is_ajax():
    q = request.GET.get('term', '')
    book = Book.objects.filter(title__icontains=q)
    results = []
    for rs in book:
      book_json = {}
      book_json = rs.title
      results.append(book_json)
    data = json.dumps(results)
  else:
    data = 'fail'
  mimetype = 'application/json'
  return HttpResponse(data, mimetype)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def login_view(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "Kullanıcı adı ya da şifre yanlış !")
            return HttpResponseRedirect('/login')
    category = Category.objects.all()
    context = {'category': category,
               }
    return render(request,'login.html',context)



def signup_view(request):
    if request.method == 'POST':
        form =SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')  # formdan bilgi al
            password = form.cleaned_data.get('password1')
            user=authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect('/')

    form = SignUpForm()
    category = Category.objects.all()
    context = {'category': category,
                   'form' : form,
                   }
    return render(request, 'signup.html', context)


def faq(request):
    category = Category.objects.all()
    faq=FAQ.objects.all().order_by('ordernumber')
    context ={
        'category':category,
        'faq':faq,

    }
    return render(request, 'faq.html', context)
