from django.db import models

class Images(models.Model):
    image = models.ImageField(upload_to='media/')


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

    name = models.CharField(max_length=200,choices=DAMAGE_PARTS_NAME_CHOICES)
    damagetype = models.CharField(max_length=20,choices=DAMAGE_PARTS_TYPE_CHOICES)


class CarSaleAd(models.Model):
    adname = models.CharField(max_length=150,null=False,blank=False)
    images = models.ForeignKey(Images,null=False,blank=False)
    price = models.IntegerField(null=False,blank=False)
    damage = models.ForeignKey(Damage,null=True,blank=True)
    tramer = models.IntegerField(null=True,blank=True)
    numberplate = models.CharField(max_length=10,null=True,blank=True)
    brand = models.CharField()
    model = models.CharField()
    modelyear = models.IntegerField(max_length=4,null=False,blank=False)


