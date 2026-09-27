from django.db import migrations


def sanitize_content(apps, schema_editor):
    # CKEditor döneminden kalan içerikleri yeni editörün izin verdiği HTML'e indirger.
    from django_prose_editor.fields import create_sanitizer
    from article.models import CONTENT_EXTENSIONS

    sanitize = create_sanitizer(CONTENT_EXTENSIONS)
    Article = apps.get_model("article", "Article")
    for article in Article.objects.only("id", "content"):
        cleaned = sanitize(article.content)
        if cleaned != article.content:
            Article.objects.filter(pk = article.pk).update(content = cleaned)


class Migration(migrations.Migration):

    dependencies = [
        ("article", "0003_alter_article_image"),
    ]

    operations = [
        migrations.RunPython(sanitize_content, migrations.RunPython.noop),
    ]
