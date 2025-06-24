from django import forms
from .models import CustomUser

class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email','first_name','last_name','profilepicture','biography','gsmnumber']

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