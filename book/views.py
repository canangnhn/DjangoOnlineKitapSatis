from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from book.models import CommentForm, Comment


def index(request):
    text="Merhaba Django";

    #return HttpResponse("Product Page")

@login_required(login_url='/login')

def addcomment(request,id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form= CommentForm(request.POST)
        if form.is_valid():
            current_user=request.user #login olan user den gelecek

            data=Comment() #model ile baglantı
            data.user_id = current_user.id
            data.book_id = id
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.ip =request.META.get('REMOTE_ADDR') #ip adresini aldık
            data.save() #veritabanına kaydet
            messages.success(request, "Yorumunuz basari ile gönderilmiştir.Teşekkür Ederiz")

            return HttpResponseRedirect(url)
    messages.error(request, "Yorumunuz gönderilememiştir.Lütfen kontrol ediniz")
    return HttpResponse("url")



