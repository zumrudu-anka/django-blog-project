import html
import math

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.html import strip_tags
from django.utils.text import Truncator
from django_prose_editor.fields import ProseEditorField


# Editörde açık olan biçimlendirmeler. Sunucu tarafında da yalnızca bunların
# ürettiği etiketlere izin verilir; geri kalan her şey (script, onerror vb.)
# kaydedilirken temizlenir.
CONTENT_EXTENSIONS = {
    "Bold": True,
    "Italic": True,
    "Underline": True,
    "Strike": True,
    "Code": True,
    "CodeBlock": True,
    "Heading": {"levels": [2, 3, 4]},
    "BulletList": True,
    "OrderedList": True,
    "ListItem": True,
    "Blockquote": True,
    "HorizontalRule": True,
    "HardBreak": True,
    "Link": {"enableTarget": False, "protocols": ["http", "https", "mailto"]},
    "Figure": True,
    "Caption": True,
    "Image": True,
}


class Article(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, verbose_name = 'Yazar')
    title = models.CharField(max_length = 50, verbose_name = 'Başlık')
    content = ProseEditorField(verbose_name="İçerik", extensions = CONTENT_EXTENSIONS, sanitize = True)
    created_date = models.DateTimeField(auto_now_add=True,verbose_name='Oluşturulma Tarihi')
    image = models.ImageField(blank = True, null = True, verbose_name="Kapak Fotoğrafı")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("article:detail", kwargs = {"id": self.id})

    @property
    def plain_text(self):
        return html.unescape(strip_tags(self.content)).replace("\xa0", " ")

    @property
    def excerpt(self):
        return Truncator(self.plain_text).words(30)

    @property
    def reading_time(self):
        return max(1, math.ceil(len(self.plain_text.split()) / 200))

    class Meta:
        db_table = 'Article'
        ordering = ["-created_date"]
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name = "Makale", related_name = "comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, verbose_name = "Kullanıcı")
    contents = models.CharField(max_length = 200, verbose_name = "Yorum")
    date = models.DateTimeField(auto_now_add = True, verbose_name = "Yorum Tarihi")

    def __str__(self):
        return "{} - {}".format(self.author, self.article)

    class Meta:
        db_table = "Comment"
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ["-date"]
