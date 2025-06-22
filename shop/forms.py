from django import forms
from .models import CarSaleAd, Images, Damage, CarBrand, CarModel

class CarBrandForm(forms.ModelForm):
    class Meta:
        model = CarBrand
        fields = ['brandname']



class CarModelBrandForm(forms.ModelForm):
    class Meta:
        model = CarModel
        fields = ['modelname']



class CarModelForm(forms.ModelForm):
    class Meta:
        model = CarSaleAd
        fields = ['brand','model']



class DamageForm(forms.ModelForm):
    class Meta:
        model = Damage
        fields = ['name','damagetype']


        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            if self.instance and self.instance.pk:
                # Güncelleme formuysa bazı alanları zorunlu yapma
                self.fields['name'].required = False
                self.fields['damagetype'].required = False



class CarSaleAdForm(forms.ModelForm):
    class Meta:
        model = CarSaleAd
        fields = ['adname','startingprice','tramer','numberplate','targetime','adescription']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            # Güncelleme formuysa bazı alanları zorunlu yapma
            self.fields['adname'].required = False
            self.fields['startingprice'].required = False
            self.fields['tramer'].required = False
            self.fields['numberplate'].required = False
            self.fields['targetime'].required = False
            self.fields['adescription'].required = False



class ImagesForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ['image']


        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            if self.instance and self.instance.pk:
                # Güncelleme formuysa bazı alanları zorunlu yapma
                self.fields['image'].required = False