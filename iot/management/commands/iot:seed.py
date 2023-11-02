import os
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


def loaddata(file):
    if os.path.splitext(file)[1] == '.json':
        instance.stdout.write(self.style.SUCCESS(file))
        os.system("python manage.py loaddata %s" % file)


class Command(BaseCommand):
    help = 'Seed database'

    def handle(self, *args, **options):
        seedfodler = os.path.join(settings.BASE_DIR, 'iot', 'seed')
        files = os.listdir(seedfodler)
        self.stdout.write(self.style.WARNING(seedfodler))
        for file in files:
            if os.path.splitext(file)[1] == '.json':
                self.stdout.write(self.style.SUCCESS(
                    "%s:" % file))
                os.system(
                    "python -Xutf8 manage.py loaddata iot/seed/%s" % file)
