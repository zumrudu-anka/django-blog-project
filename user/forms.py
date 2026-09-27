import time

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core import signing

User = get_user_model()

# Formu bundan daha hızlı dolduran büyük olasılıkla bir bottur.
MIN_FILL_SECONDS = 3
FORM_TOKEN_SALT = "user.register"


class LoginForm(forms.Form):
    username = forms.CharField(max_length = 50, label="Kullanıcı adı",
        widget = forms.TextInput(attrs = {"autocomplete": "username", "autofocus": True}))
    password = forms.CharField(max_length = 128, label = "Parola",
        widget = forms.PasswordInput(attrs = {"autocomplete": "current-password"}))


class RegisterForm(forms.Form):
    username = forms.CharField(min_length = 3, max_length = 30, label="Kullanıcı adı",
        validators = [UnicodeUsernameValidator()],
        help_text = "Harf, rakam ve @ . + - _ karakterleri kullanılabilir.",
        widget = forms.TextInput(attrs = {"autocomplete": "username", "autofocus": True}))
    password = forms.CharField(max_length = 128, label = "Parola",
        help_text = "En az 8 karakter; tamamı rakam veya çok yaygın bir parola olmamalı.",
        widget = forms.PasswordInput(attrs = {"autocomplete": "new-password"}))
    confirm = forms.CharField(max_length = 128, label = "Parolayı doğrula",
        widget = forms.PasswordInput(attrs = {"autocomplete": "new-password"}))

    # Bot tuzakları: `website` insanlara gösterilmez (bkz. form_fields.html),
    # `started` ise formun ne zaman açıldığını imzalı olarak taşır.
    website = forms.CharField(required = False, label = "Web sitesi",
        widget = forms.TextInput(attrs = {"autocomplete": "off", "tabindex": "-1"}))
    started = forms.CharField(widget = forms.HiddenInput)

    honeypot_fields = ("website",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["started"].initial = signing.dumps(time.time(), salt = FORM_TOKEN_SALT)

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username__iexact = username).exists():
            raise forms.ValidationError("Bu kullanıcı adı zaten alınmış.")
        return username

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get("website"):
            raise forms.ValidationError("Kayıt tamamlanamadı, lütfen tekrar deneyin.")
        try:
            started = signing.loads(cleaned_data.get("started", ""), salt = FORM_TOKEN_SALT, max_age = 60 * 60)
        except signing.BadSignature:
            raise forms.ValidationError("Formun süresi doldu, lütfen sayfayı yenileyip tekrar deneyin.")
        if time.time() - started < MIN_FILL_SECONDS:
            raise forms.ValidationError("Kayıt tamamlanamadı, lütfen tekrar deneyin.")

        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm")
        if password and confirm and password != confirm:
            self.add_error('confirm', "Parolalar eşleşmiyor.")
        elif password:
            try:
                validate_password(password, User(username = cleaned_data.get("username", "")))
            except forms.ValidationError as error:
                self.add_error('password', error)
        return cleaned_data
