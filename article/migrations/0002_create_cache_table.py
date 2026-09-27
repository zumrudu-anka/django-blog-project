from django.core.management import call_command
from django.db import migrations


def create_cache_table(apps, schema_editor):
    # Hız sınırlayıcı (blog/ratelimit.py) veritabanı cache'ini kullanır. Tabloyu
    # migrate'in oluşturması, başlatma komutunda ayrı bir adıma bağımlı kalmamayı
    # sağlar. Komut tablo zaten varsa bir şey yapmaz.
    call_command("createcachetable", database = schema_editor.connection.alias, verbosity = 0)


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_cache_table, migrations.RunPython.noop),
    ]
