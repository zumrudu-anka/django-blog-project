from django import forms
from django.contrib.auth.models import User
class RegisterForm(forms.Form):
    username = forms.CharField(max_length = 50, label="Kullanıcı Adı")
    password = forms.CharField(max_length = 20, label = "Parola", widget = forms.PasswordInput)
    confirm = forms.CharField(max_length= 20, label = "Parolayı Doğrula", widget = forms.PasswordInput)
    
    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        confirm  = self.cleaned_data.get("confirm")
        if password and confirm and password != confirm:
            self.add_error('confirm', "Parolalar Eşleşmiyor!")
        elif User.objects.filter(username = username).count() > 0:
            self.add_error('username', "Kullanıcı Zaten Mevcut!")
        return super(RegisterForm, self).clean()
