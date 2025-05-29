from django import forms
from .models import CarSaleAd, Images, Damage, CarBrand

class CarBrandForm(forms.ModelForm):
    class Meta:
        model = CarBrand
        fields = ['brandname']



class CarModelForm(forms.ModelForm):
    class Meta:
        model = CarSaleAd
        fields = ['brand','model']



class DamageForm(forms.ModelForm):
    class Meta:
        model = Damage
        fields = ['name','damagetype']



class CarSaleAdForm(forms.ModelForm):
    class Meta:
        model = CarSaleAd
        fields = ['adname','startingprice','tramer','numberplate','targetime','adescription','images']



class ImagesForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ['image']