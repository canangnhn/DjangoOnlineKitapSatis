"""mydjangoproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from home import views
from order import views as orderviews

urlpatterns = [
    path('', include('home.urls')),
    path('home/', include('home.urls')),
    path('book/', include('book.urls')),
    path('user/', include('user.urls')),
    path('order/', include('order.urls')),
    path('hakkimizda/',views.hakkimizda, name='hakkimizda'),
    path('referanslar/', views.referanslar, name='referanslar'),
    path('iletisim/', views.iletisim, name='iletisim'),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('category/<int:id>/<slug:slug>/', views.category_books, name='category_books'),
    path('book/<int:id>/<slug:slug>/', views.book_detail, name='book_detail'),
    path('search/',views.book_search,name='book_search'),
    path('search_auto/',views.book_search_auto,name='book_search_auto'),
    path('logout/',views.logout_view,name='logout_view,'),
    path('login/', views.login_view, name='login_view,'),
    path('signup/', views.signup_view, name='signup_view,'),
    path('shopcart/', orderviews.shopcart, name='shopcart,'),
    path('sss/', views.faq, name='faq',),
]
if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)