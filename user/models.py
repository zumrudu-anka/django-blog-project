from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    """
    Django'nun hazır kullanıcı modeli + profil alanları. Ad/soyad
    (first_name/last_name) AbstractUser'da zaten var.
    """
    avatar = models.ImageField(upload_to = "avatars/", blank = True, null = True, verbose_name = "Profil fotoğrafı")
    bio = models.CharField(max_length = 300, blank = True, verbose_name = "Hakkında")

    class Meta(AbstractUser.Meta):
        db_table = "User"
        swappable = "AUTH_USER_MODEL"

    @property
    def display_name(self):
        """Ad soyad girilmişse onu, yoksa kullanıcı adını döndürür."""
        return self.get_full_name() or self.username

    def get_absolute_url(self):
        return reverse("user:profile", kwargs = {"username": self.username})
