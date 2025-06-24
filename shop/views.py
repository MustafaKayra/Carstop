from django.shortcuts import render, redirect
from .models import CarSaleAd, Damage, CarBrand, CarModel, Images, Bid
from .forms import CarModelForm, DamageForm, CarSaleAdForm, ImagesForm, CarBrandForm, CarModelBrandForm
from django.core.exceptions import ValidationError
from .utils import get_countdown_data, email_send_data
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings

def index(request):
    ads = CarSaleAd.objects.filter(is_active=True)
    context = {
        "ads": ads
    }
    return render(request, "index.html", context)


def adpost(request):
    step = 1
    form1 = CarBrandForm()
    form2 = DamageForm()
    form4 = ImagesForm()
    form3 = CarSaleAdForm()
    form5 = CarModelBrandForm()
    carbrand = CarBrand.objects.all()
    modelobject = CarModel.objects.none()
    partsname = Damage.DAMAGE_PARTS_NAME_CHOICES
    damagedparts = Damage.DAMAGE_PARTS_TYPE_CHOICES
    adobjectcontext = request.session.get('adobject_id')
    damagedpart = None
    imageobjects = None

    if adobjectcontext is None:
        adobjectcontext = None


    if request.method == "POST":

        if "form1" in request.POST:
            form1 = CarBrandForm(request.POST)
            if form1.is_valid():
                brandname = form1.cleaned_data.get("brandname")
                brandobject = CarBrand.objects.get(brandname=brandname)

                request.session['brand_id'] = brandobject.id

                modelobject = CarModel.objects.filter(brand=brandobject)
                step = 2
                print(brandname)
                print(brandobject)
                print(modelobject)
                print(step)
                

        elif "form5" in request.POST:
            form5 = CarModelBrandForm(request.POST)
            if form5.is_valid():
                modelname = form5.cleaned_data.get("modelname")
                model = CarModel.objects.get(modelname=modelname)

                request.session['model_id'] = model.id

                step = 3
                print(modelname)
                print(model)

            

        elif "form3" in request.POST:
            form3 = CarSaleAdForm(request.POST)
            if form3.is_valid():
                adname = form3.cleaned_data.get("adname")
                startingprice = form3.cleaned_data.get("startingprice")
                tramer = form3.cleaned_data.get("tramer")
                numberplate = form3.cleaned_data.get("numberplate")
                targetime = form3.cleaned_data.get("targetime")
                adescription = form3.cleaned_data.get("adescription")
                advertiser = request.user

                brand_id = request.session.get("brand_id")
                model_id = request.session.get("model_id")

                brand = CarBrand.objects.get(id=brand_id)
                modelobjects = CarModel.objects.get(id=model_id)

                adobject = CarSaleAd.objects.create(adname=adname,startingprice=startingprice,tramer=tramer,numberplate=numberplate,brand=brand,model=modelobjects,targetime=targetime,adescription=adescription,advertiser=advertiser)
                request.session['adobject_id'] = adobject.id
                print("İlan Oluşturuldu")
                step = 4
            else:
                print(form3.errors)

        
        elif "form2" in request.POST:
            form2 = DamageForm(request.POST)
            if form2.is_valid():
                name = form2.cleaned_data.get("name")
                damagetype = form2.cleaned_data.get("damagetype")
                adobject_id = request.session.get("adobject_id")
                adobject = CarSaleAd.objects.get(id=adobject_id)

                damage = Damage.objects.create(name=name,damagetype=damagetype,ad=adobject)

                filterdamagedpart = Damage.objects.filter(ad=adobject, name=request.POST.get("name")) #Eğer daha önce kaydedilen parçalar ile formda kaydedilen parça aynı ise aynı isime sahip parçalar filtreleniyor
                if filterdamagedpart.count() > 1:
                    filterdamagedpart.delete()
                    raise ValidationError("Parça Çakışması")
                

                damagedpart = Damage.objects.filter(ad=adobject)
                step = 4
                print(damage)
            else:
                print(form2.errors)

        elif "step5" in request.POST:
            step = 5
            print(step)
            print("Step Değeri Güncellendi")



        elif "deletepart" in request.POST:
            part_id = request.POST.get("delete_part")
            adobject_id = request.session.get("adobject_id")
            adobject = CarSaleAd.objects.get(id=adobject_id)
            part = Damage.objects.get(id=part_id, ad=adobject)
            part.delete()
            damagedpart = Damage.objects.filter(ad=adobject)
            step = 4
            print("Parça Başarıyla Silindi")

            

        elif request.method == "POST" and request.FILES.get("image"):
            form4 = ImagesForm(request.POST, request.FILES)
            if form4.is_valid():
                image = form4.save(commit=False)
                adobject_id = request.session.get('adobject_id')
                adobject = CarSaleAd.objects.get(id=adobject_id)
                image.ad = adobject
                image.save()
                print("Resim Kaydedildi")
                print(f"resimin kayıt olduğu ilan: {image.ad}, resim: {image.image}")

                imageobjects = Images.objects.filter(ad=adobject)

                step = 5
            else:
                print(form4.errors)



        elif "deleteimage" in request.POST:
            image_id = request.POST.get("delete_image")
            adobject_id = request.session.get("adobject_id")
            adobject = CarSaleAd.objects.get(id=adobject_id)
            images = Images.objects.get(id=image_id, ad=adobject_id)
            images.delete()
            imageobjects = Images.objects.filter(ad=adobject)
            step = 5
            print("Resim Silindi")


        
                
        elif "step6" in request.POST:
            return redirect('index')
        


        context = {
            'carbrand': carbrand,
            'form1': form1,
            'form2': form2,
            'form4': form4,
            'form3': form3,
            'step': step,
            'modelobject': modelobject,
            'partsname': partsname,
            'damagedparts': damagedparts,
            'adobjectcontext': adobjectcontext,
            'damagedpart': damagedpart,
            'imageobjects': imageobjects
        }
        return render(request,"adpost.html",context)
    
    else:
        context = {
            'carbrand': carbrand,
            'form1': form1,
            'form2': form2,
            'form4': form4,
            'form3': form3,
            'step': step,
            'modelobject': modelobject,
            'partsname': partsname,
            'damagedparts': damagedparts,
            'adobjectcontext': adobjectcontext,
            'damagedpart': damagedpart,
            'imageobjects': imageobjects
        }
        return render(request,"adpost.html",context)
    


def adetail(request,slug):
    ad = CarSaleAd.objects.get(slug=slug,is_active=True)
    countdown = get_countdown_data(ad)
    email_send = email_send_data(ad)

    images = ad.images_set.all()  # Bu ilanla ilişkili tüm resimleri al

    damagedparts = Damage.objects.filter(ad=ad)
    print(f"Damaged parts: {damagedparts}")

    if request.method == "POST":
        newprice = request.POST.get("price")
        if int(newprice) > ad.startingprice:
            if request.user == ad.advertiser:
                print("Kullanıcı Kendi İlanına Fiyat Teklifi Yapamaz")
                return redirect('index')
            else:
                ad.startingprice = newprice
                ad.save()

                Bid.objects.create(ad=ad, user=request.user, amount=newprice)
                send_mail(
                    subject="İlanınıza Yeni Bir Teklif Geldi!",
                    message=f"""{ad.adname} İlanınıza {newprice} değerinde yeni bir teklif geldi
                    
                    İLAN DETAYLARI:
                    İlan İsmi: {ad.adname}
                    İlan Bitiş Tarihi: {ad.targetime}
                    İlan Güncel Fiyatı: {ad.startingprice}
                    Araç Plakası: {ad.numberplate}
                    Araç Model: {ad.model}

                    """,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[ad.advertiser.email],
                    fail_silently=False,
                )
                print("İlan Fiyatı Güncellendi")
        else:
            print("Önerilen Fiyat, Güncel Fiyattan Küçük Olamaz!")

    context = {
        "ad": ad,
        "images": images,
        "damagedparts": damagedparts,
        "countdown": countdown,
        "email_send": email_send
    }
    return render(request,"adetail.html",context)



def updatead(request, slug):
    ad = CarSaleAd.objects.get(slug=slug)
    partsname = Damage.DAMAGE_PARTS_NAME_CHOICES
    damagedparts = Damage.DAMAGE_PARTS_TYPE_CHOICES
    adobjectcontext = request.session.get('adobject_id')

    if adobjectcontext is None:
        adobjectcontext = None
    else:
        adobject = CarSaleAd.objects.get(id=adobjectcontext)
        print(f"GET İSTEĞİ: {adobject}")
    
    form2 = DamageForm()
    form4 = ImagesForm()
    form3 = CarSaleAdForm()
    damagedpart = Damage.objects.filter(ad=ad)
    imageobjects = Images.objects.filter(ad=ad)
    step = 3

    if request.method == "POST":
        
        if "form3" in request.POST:
            form3 = CarSaleAdForm(request.POST, instance=ad)
            request.session['adobject_startingprice'] = ad.startingprice
            ad_startingprice = request.session.get("adobject_startingprice")
            if form3.is_valid():
                newad = form3.save(commit=False)
                bid = Bid.objects.filter(ad=ad)
                if bid:
                    newad.startingprice = ad_startingprice
                    print("Fiyat Teklifi Verilen Bir İlan Fiyatı Güncellenemez")
                    newad.advertiser = request.user
                    newad.save()
                else:
                    newad.advertiser = request.user
                    newad.save()

                request.session['adobject_id'] = newad.id
                print("İlan Güncellendi")
                step = 4
            else:
                print(form3.errors)

        
        elif "form2" in request.POST:
            form2 = DamageForm(request.POST, instance=ad)
            if form2.is_valid():
                name = form2.cleaned_data.get("name")
                damagetype = form2.cleaned_data.get("damagetype")
                adobject_id = request.session.get("adobject_id")
                adobject = CarSaleAd.objects.get(id=adobject_id)

                damage = Damage.objects.create(name=name,damagetype=damagetype,ad=adobject)

                filterdamagedpart = Damage.objects.filter(ad=adobject, name=request.POST.get("name")) #Eğer daha önce kaydedilen parçalar ile formda kaydedilen parça aynı ise aynı isime sahip parçalar filtreleniyor
                if filterdamagedpart.count() > 1:
                    filterdamagedpart.delete()
                    raise ValidationError("Parça Çakışması")
                

                damagedpart = Damage.objects.filter(ad=adobject)
                step = 4
                print(damage)
            else:
                print(form2.errors)

        elif "step5" in request.POST:
            step = 5
            print(step)
            print("Step Değeri Güncellendi")



        elif "deletepart" in request.POST:
            part_id = request.POST.get("delete_part")
            adobject_id = request.session.get("adobject_id")
            adobject = CarSaleAd.objects.get(id=adobject_id)
            part = Damage.objects.get(id=part_id, ad=adobject)
            part.delete()
            damagedpart = Damage.objects.filter(ad=adobject)
            step = 4
            print("Parça Başarıyla Silindi")

            

        elif request.method == "POST" and request.FILES.get("image"):
            form4 = ImagesForm(request.POST, request.FILES)
            imageobjects = Images.objects.filter(ad=adobject)
            if form4.is_valid():
                image = form4.save(commit=False)
                adobject_id = request.session.get('adobject_id')
                adobject = CarSaleAd.objects.get(id=adobject_id)
                image.ad = adobject
                image.save()
                print(f"resimin kayıt olduğu ilan: {image.ad}, resim: {image.image}")
                print("Resim Kaydedildi")

                imageobjects = Images.objects.filter(ad=adobject)

                step = 5
            else:
                print(form4.errors)



        elif "deleteimage" in request.POST:
            image_id = request.POST.get("delete_image")
            adobject_id = request.session.get("adobject_id")
            adobject = CarSaleAd.objects.get(id=adobject_id)
            images = Images.objects.get(id=image_id, ad=adobject_id)
            images.delete()
            imageobjects = Images.objects.filter(ad=adobject)
            step = 5
            print("Resim Silindi")


        
                
        elif "step6" in request.POST:
            return redirect('index')
        


        context = {
            'form2': form2,
            'form4': form4,
            'form3': form3,
            'step': step,
            'partsname': partsname,
            'damagedparts': damagedparts,
            'adobjectcontext': adobjectcontext,
            'damagedpart': damagedpart,
            'imageobjects': imageobjects,
            "ad": ad
        }
        return render(request,"adpost.html",context)
    
    else:
        context = {
            'form2': form2,
            'form4': form4,
            'form3': form3,
            'step': step,
            'partsname': partsname,
            'damagedparts': damagedparts,
            'adobjectcontext': adobjectcontext,
            'damagedpart': damagedpart,
            'imageobjects': imageobjects,
            "ad": ad
        }
    return render(request,"updatead.html", context)