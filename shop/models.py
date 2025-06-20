from django.db import models
from django.conf import settings
from django.utils.text import slugify


class CarBrand(models.Model): #Admin paneli üzerinden yönetici tarafından eklenecek
    brandname = models.CharField(max_length=30,null=False,blank=False)
    image = models.ImageField()

    class Meta:
        verbose_name = "Araba Markası"
        verbose_name_plural = "Araba Markaları"

    def __str__(self):
        return f"{self.brandname}"
    

class FuelType(models.Model): #Admin paneli üzerinden yönetici tarafından eklenecek
    fueltype = models.CharField(max_length=20,null=False,blank=False)

    class Meta:
        verbose_name = "Yakıt Türü"
        verbose_name_plural = "Yakıt Türleri"

    def __str__(self):
        return f"{self.fueltype}"


class CarModel(models.Model): #Admin paneli üzerinden yönetici tarafından eklenecek
    brand = models.ForeignKey(CarBrand,null=False,blank=False,on_delete=models.CASCADE)
    modelname = models.CharField(max_length=100,null=False,blank=False)
    modelyear = models.IntegerField(null=False,blank=False)
    fueltype = models.ForeignKey(FuelType,null=False,blank=False,on_delete=models.CASCADE)
    enginesize = models.IntegerField(null=False,blank=False) #Aracın motor hacmi
    enginepower = models.CharField(max_length=6,null=False,blank=False) #Aracın Motor gücü
    image = models.ImageField(upload_to='media/')

    class Meta:
        verbose_name = "Araba Modeli"
        verbose_name_plural = "Araba Modelleri"

    def __str__(self):
        return f"{self.brand} | {self.modelname} | {self.modelyear} | {self.fueltype} | {self.enginesize}"


class CarSaleAd(models.Model):
    adname = models.CharField(max_length=150,null=False,blank=False) # İlan ismi
    startingprice = models.IntegerField(null=False,blank=False) #İlan fiyatı
    tramer = models.IntegerField(null=True,blank=True) #İlandaki aracın tramer kaydı
    numberplate = models.CharField(max_length=10,null=True,blank=True) #İlandaki aracın plakası
    brand = models.ForeignKey(CarBrand,null=False,blank=False,on_delete=models.CASCADE) #Aracın markası
    model = models.ForeignKey(CarModel,null=False,blank=False,on_delete=models.CASCADE) #Aracın modeli
    targetime = models.DateTimeField(null=False,blank=False)
    adescription = models.TextField() #İlan açıklaması
    advertiser = models.ForeignKey(settings.AUTH_USER_MODEL,null=False,blank=False,on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(null=True,blank=True,unique=True,db_index=True)

    class Meta:
        verbose_name = "Araba İlanı"
        verbose_name_plural = "Araba İlanları"

    def __str__(self):
        return f"{self.adname}"
    
    def save(self, *args, **kwargs):
        creating = self.pk is None
        super().save(*args, **kwargs)

        if creating:
            self.slug = slugify(f"{self.adname}-{self.id}")
            # Slug değeri değiştiyse tekrar kaydet
            self.save(update_fields=["slug"])
    


class Damage(models.Model):
    DAMAGE_PARTS_NAME_CHOICES = [
        ('part1', 'Ön Tampon'),
        ('part2', 'Kaput'),
        ('part3', 'Sağ Ön Çamurluk'),
        ('part4', 'Sol Ön Çamurluk'),
        ('part5', 'Sağ Ön Kapı'),
        ('part6', 'Sol Ön Kapı'),
        ('part7', 'Sağ Arka Kapı'),
        ('part8', 'Sol Arka Kapı'),
        ('part9', 'Sağ Arka Çamurluk'),
        ('part10', 'Sol Arka Çamurluk'),
        ('part11', 'Arka Tampon'),
        ('part12', 'Bagaj Kapağı'),
        ('part13', 'Tavan')
    ]

    DAMAGE_PARTS_TYPE_CHOICES = [
        ('painted', 'Boyalı'),
        ('locally', 'Lokal Boyalı'),
        ('changing', 'Değişen')
    ]    

    ad = models.ForeignKey(CarSaleAd,null=False,blank=False,on_delete=models.CASCADE)
    name = models.CharField(max_length=200,choices=DAMAGE_PARTS_NAME_CHOICES)
    damagetype = models.CharField(max_length=20,choices=DAMAGE_PARTS_TYPE_CHOICES)

    class Meta:
        verbose_name = "Hasarlı Parça"
        verbose_name_plural = "Hasarlı Parçalar"



class Images(models.Model):
    ad = models.ForeignKey(CarSaleAd,null=False,blank=False,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/')

    class Meta:
        verbose_name = "Araç İlan Resmi"
        verbose_name_plural = "Araç İlan Resimleri"



class Bid(models.Model):
    ad = models.ForeignKey(CarSaleAd, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.IntegerField(null=False,blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Fiyat Teklifi"
        verbose_name_plural = "Fiyat Teklifleri"

    def __str__(self):
        return f"{self.user.email} - {self.amount} TL"