from django.db import models
from ckeditor.fields import RichTextField
class Article(models.Model):
    author = models.ForeignKey("auth.User", on_delete = models.CASCADE, verbose_name = 'Yazar')
    title = models.CharField(max_length = 50, verbose_name = 'Başlık')
    content = RichTextField(verbose_name="İçerik")
    created_date = models.DateTimeField(auto_now_add=True,verbose_name='Oluşturulma Tarihi')
    image = models.FileField(blank = True, null = True, verbose_name="Fotoğraf Ekleyin")
    def __str__(self):
        return self.title