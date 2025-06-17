from django import forms
from .models import CustomUser

class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email','first_name','last_name','profilepicture','biography','gsmnumber']