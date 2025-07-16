from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate,logout
from .forms import UserForm
from .models import CustomUser
from shop.models import CarSaleAd, Bid
from django.contrib import messages

def createuser(request):
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            print(f"Yeni Kullanıcı: {user}")
            return redirect('index')
        else:
            messages.warning(request,form.errors)
    else:
        form = UserForm()
    return render(request,"createuser.html",{"form": form})



def loginuser(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(email=email,password=password)

        if user:
            login(request, user)
            messages.success(request,"Kullanıcı Girişi Yapıldı")
            return redirect('index')
        else:
            messages.warning(request,"Kullanıcı Bulunamadı")
    return render(request,"loginuser.html")



def updateuser(request):
    user_id = request.user.id
    user = CustomUser.objects.get(id=user_id)

    if request.method == "POST":
        if request.user:
            form = UserForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                newuser = form.save()
                login(request, newuser)
                messages.success(request,"Değişiklikler Kaydedildi")
                return redirect('index')
            else:
                messages.warning(request,form.errors)
        else:
            return redirect('loginuser')
    else:
        form = UserForm(instance=user)
    return render(request,"updateuser.html",{"form": form, "user": user})



def detailuser(request, id):
    if request.user:
        user = CustomUser.objects.get(id=id)
        usergetad = CarSaleAd.objects.filter(advertiser=user)
    else:
        messages.warning(request,"Herhangi Bir Profile Sahip Değilsiniz!")
        return redirect('loginuser')
    
    context = {
        "user": user,
        "usergetad": usergetad
    }
    return render(request,"detailuser.html",context)



def bids(request):
    if request.user:
        ads = CarSaleAd.objects.filter(bid__user=request.user).distinct()
        bid_objects = Bid.objects.filter(user=request.user, ad__in=ads)
    else:
        messages.warning(request,"Herhangi Bir Profile Sahip Değilsiniz!")
        return redirect('loginuser')
    

    context = {
        "bid_objects": bid_objects,
        "ads": ads
    }
    return render(request,"bids.html",context)