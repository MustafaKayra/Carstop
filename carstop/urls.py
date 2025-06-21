from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from shop import views
from users import views as users_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('shop/',include('shop.urls')),
    path('',views.index,name="index"),
    path('publishcar/',views.adpost,name="adpost"),
    path('ad/<slug:slug>',views.adetail,name="adetail"),
    path('createuser/',users_views.createuser,name="createuser"),
    path('loginuser/',users_views.loginuser,name="loginuser"),
    path('updateuser/',users_views.updateuser,name="updateuser"),
    path('detailuser/<int:id>',users_views.detailuser,name="detailuser")
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
