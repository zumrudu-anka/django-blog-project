import io
import time

from PIL import Image, ImageOps

from django import forms
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core import signing

User = get_user_model()

# Formu bundan daha hızlı dolduran büyük olasılıkla bir bottur.
MIN_FILL_SECONDS = 3
FORM_TOKEN_SALT = "user.register"

AVATAR_MAX_BYTES = 5 * 1024 * 1024
AVATAR_MAX_PIXELS = 40_000_000
AVATAR_SIZE = 400


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "bio", "avatar"]
        labels = {"first_name": "Ad", "last_name": "Soyad"}
        help_texts = {
            "bio": "Yazılarının altında ve profilinde görünür. En fazla 300 karakter.",
            "avatar": "JPG, PNG veya WEBP, en fazla 5 MB. Kare olarak kırpılır.",
        }
        widgets = {
            "bio": forms.Textarea(attrs = {"rows": 3, "maxlength": 300}),
            "avatar": forms.ClearableFileInput(attrs = {"accept": "image/jpeg,image/png,image/webp"}),
        }

    def clean_avatar(self):
        avatar = self.cleaned_data.get("avatar")
        # Yeni dosya yüklenmediyse (mevcut fotoğraf ya da "temizle") dokunma.
        if not avatar or not hasattr(avatar, "content_type"):
            return avatar
        if avatar.size > AVATAR_MAX_BYTES:
            raise forms.ValidationError("Fotoğraf en fazla 5 MB olabilir.")

        try:
            image = Image.open(avatar)
        except Exception:
            raise forms.ValidationError("Bu dosya okunabilir bir resim değil.")
        # Küçük dosya boyutu küçük resim demek değil: 1 MB'lık bir PNG yüz milyonlarca
        # piksele açılıp sunucu belleğini doldurabilir. Açmadan önce çözünürlüğe bak.
        if image.width * image.height > AVATAR_MAX_PIXELS:
            raise forms.ValidationError("Fotoğrafın çözünürlüğü çok yüksek (en fazla 40 megapiksel).")
        try:
            image.draft("RGB", (AVATAR_SIZE * 2, AVATAR_SIZE * 2))  # JPEG'i küçültülmüş çözer
            image = ImageOps.exif_transpose(image).convert("RGB")
        except Exception:
            raise forms.ValidationError("Bu dosya okunabilir bir resim değil.")

        # Ortadan kare kırp ve küçült; telefondan gelen 10 MB'lık fotoğraf ~30 KB olur.
        image = ImageOps.fit(image, (AVATAR_SIZE, AVATAR_SIZE), Image.LANCZOS)
        buffer = io.BytesIO()
        image.save(buffer, format = "JPEG", quality = 85, optimize = True)
        return InMemoryUploadedFile(
            buffer, "avatar", "{}.jpg".format(self.instance.username), "image/jpeg",
            buffer.getbuffer().nbytes, None,
        )


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
