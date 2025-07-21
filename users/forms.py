from django import forms
from django.core.validators import RegexValidator
from .models import CustomUser

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    gsmnumber = forms.CharField(
        required=False,
        validators=[
            RegexValidator(
                regex=r'^\d{10,11}$',
                message="Geçerli bir GSM numarası girin. Sadece rakam ve 10-11 hane olmalı.",
                code='invalid_gsm'
            )
        ]
    )

    class Meta:
        model = CustomUser
        fields = ['email','first_name','last_name','profilepicture','biography','gsmnumber','password']

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            # Güncelleme formuysa bazı alanları zorunlu yapma
            self.fields['email'].required = False
            self.fields['first_name'].required = False
            self.fields['last_name'].required = False
            self.fields['profilepicture'].required = False
            self.fields['biography'].required = False
            self.fields['gsmnumber'].required = False
            self.fields['password'].required = False