from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from shop import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name="index"),
    path('publishcar/',views.adpost,name="adpost"),
    path('ad/<slug:slug>',views.adetail,name="adetail")
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
