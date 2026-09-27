from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Django'nun hazır kullanıcı modeliyle birebir aynıdır; yalnızca tablo adı
    `auth_user` yerine `User` olsun diye projeye taşındı.
    """

    class Meta(AbstractUser.Meta):
        db_table = "User"
        swappable = "AUTH_USER_MODEL"
