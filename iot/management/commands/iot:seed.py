import os
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Seed database'

    def handle(self, *args, **options):
        seedfolder = os.path.join(settings.BASE_DIR, 'iot', 'seed')
        files = os.listdir(seedfolder)
        sorted_files = sorted(files)  # Ordena os nomes dos arquivos

        self.stdout.write(self.style.WARNING(seedfolder))

        for file in sorted_files:
            if os.path.splitext(file)[1] == '.json':
                self.stdout.write(self.style.SUCCESS("%s:" % file))
                os.system("python manage.py loaddata iot/seed/%s" % file)
