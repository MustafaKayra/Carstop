from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate,logout
from .forms import UserForm

def createuser(request):
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            print(f"Yeni Kullanıcı: {user}")
            return redirect('index')
        else:
            print(form.errors)
    else:
        form = UserForm()
    return render(request,"createuser.html",{"form": form})

