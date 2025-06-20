from django.contrib import admin
from .models import Images,Damage,CarBrand,CarModel,CarSaleAd,FuelType,Bid

admin.site.register(Images)
admin.site.register(Damage)
admin.site.register(CarBrand)
admin.site.register(CarModel)
admin.site.register(FuelType)
admin.site.register(CarSaleAd)
admin.site.register(Bid)
