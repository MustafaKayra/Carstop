from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.core.exceptions import ValidationError



class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError("Email alanı gereklidir")
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        user = self.create_user(email, first_name, last_name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
    

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True,verbose_name="Email")
    first_name = models.CharField(max_length=30,null=False,blank=False,verbose_name="İsim")
    last_name = models.CharField(max_length=30,null=False,blank=False,verbose_name="Soyisi")
    date = models.DateField(auto_now_add=True,verbose_name="Kullanıcı Oluşturulma Tarihi")
    profilepicture = models.ImageField(upload_to="profilepicture/",null=True,blank=True,verbose_name="Profil Fotoğrafı")
    biography = models.TextField(null=True,blank=True)
    gsmnumber = models.IntegerField(max_length=12,null=True,blank=False)
    is_active = models.BooleanField(default=True,verbose_name="Kullanıcı Aktiflik Durumu")
    is_staff = models.BooleanField(default=False,verbose_name="Kullanıcı Yönetici Paneline Giriş Yetkisi")
    is_superuser = models.BooleanField(default=False,verbose_name="Kullanıcı Yönetici Yetkisi")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["first_name","last_name"]

    objects = CustomUserManager()