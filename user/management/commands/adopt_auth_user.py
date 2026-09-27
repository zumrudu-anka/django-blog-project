from django.core.management.base import BaseCommand
from django.db import connection
from django.db.migrations.recorder import MigrationRecorder


class Command(BaseCommand):
    help = (
        "Kullanıcılar Django'nun hazır `auth_user` tablosundan projedeki `user.User` "
        "modeline taşınırken, kurulu veritabanlarında `migrate`'ten ÖNCE bir kez "
        "çalıştırılır. Tablo zaten var olduğu için `user.0001_initial` migration'ını "
        "uygulanmış olarak işaretler; ardından `migrate` tabloyu `User` olarak "
        "yeniden adlandırır. Sıfırdan kurulumda veya tekrar çalıştırıldığında bir şey yapmaz."
    )

    def handle(self, *args, **options):
        recorder = MigrationRecorder(connection)
        recorder.ensure_schema()

        if ("user", "0001_initial") in recorder.applied_migrations():
            self.stdout.write("Zaten hazır, yapılacak bir şey yok.")
            return

        if "auth_user" not in connection.introspection.table_names():
            self.stdout.write("auth_user tablosu yok (sıfırdan kurulum); doğrudan `migrate` çalıştırın.")
            return

        recorder.record_applied("user", "0001_initial")
        self.stdout.write(self.style.SUCCESS(
            "user.0001_initial uygulanmış olarak işaretlendi. Şimdi `python manage.py migrate` çalıştırın."
        ))
