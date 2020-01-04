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
    class Meta:
        db_table = 'Makale'
        #managed = True
        ordering = ["-created_date"]
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name = "Makale", related_name = "comments")
    author = models.CharField(max_length = 50, verbose_name = "İsim")
    contents = models.CharField(max_length = 200, verbose_name = "Yorum")
    date = models.DateTimeField(auto_now_add = True, verbose_name = "Yorum Tarihi")
    def __str__(self):
        return "{} - {}".format(self.author, self.article)
    class Meta:
        db_table = "Yorum"
        verbose_name = 'Yorum'
        verbose_name_plural = 'Yorumlar'
        ordering = ["-date"]