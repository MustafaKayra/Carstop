from django.shortcuts import render
from .models import CarSaleAd, Damage
from .forms import CarModelForm, DamageForm, CarSaleAdForm, ImagesForm



def adpost2(request):
    if request.method == "POST":

        if "form1" in request.POST:
            form1 = CarModelForm(request.POST)
            if form1.is_valid():
                brand = form1.cleaned_data.get("brand")
                model = form1.cleaned_data.get("model")

        elif "form2" in request.POST:
            form2 = DamageForm(request.POST)
            if form2.is_valid():
                name = form2.cleaned_data.get("name")
                damagetype = form2.cleaned_data.get("damagetype")
                damage = Damage.objects.create(name=name,damagetype=damagetype)

        elif "form4" in request.POST:
            form4 = ImagesForm(request.POST, request.FILES)
            if form4.is_valid():
                
                image_instance = form4.save(commit=False)
                image_instance.save()
                request.session['image_ins'] = image_instance.id

        elif "form3" in request.POST:
            form3 = CarSaleAdForm(request.POST)
            if form3.is_valid():
                adname = form3.cleaned_data.get("adname")
                startingprice = form3.cleaned_data.get("startingprice")
                tramer = form3.cleaned_data.get("tramer")
                numberplate = form3.cleaned_data.get("numberplate")
                targetime = form3.cleaned_data.get("targetime")
                adescription = form3.cleaned_data.get("adescription")

                image_instances = request.session.get('image_ins')
                advertiser = request.user

                CarSaleAd.objects.create(adname=adname,images=image_instances,startingprice=startingprice,damage=damage,tramer=tramer,numberplate=numberplate,brand=brand,model=model,targetime=targetime,adescription=adescription,advertiser=advertiser)
                print("İlan Oluşturuldu")
    
    else:
        return render(request,"adpost.html")

        