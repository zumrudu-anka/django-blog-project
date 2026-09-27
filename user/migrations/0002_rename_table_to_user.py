from django.db import migrations


def move_content_type(apps, schema_editor):
    # Mevcut izinler ve admin kayıtları "auth | user" içerik tipine bağlı.
    # Tipi yeni uygulamaya taşıyınca hepsi yeni modelle çalışmaya devam eder.
    ContentType = apps.get_model("contenttypes", "ContentType")
    if not ContentType.objects.filter(app_label = "user", model = "user").exists():
        ContentType.objects.filter(app_label = "auth", model = "user").update(app_label = "user")


def restore_content_type(apps, schema_editor):
    ContentType = apps.get_model("contenttypes", "ContentType")
    if not ContentType.objects.filter(app_label = "auth", model = "user").exists():
        ContentType.objects.filter(app_label = "user", model = "user").update(app_label = "auth")


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='user',
            table='User',
        ),
        migrations.RunPython(move_content_type, restore_content_type),
    ]
