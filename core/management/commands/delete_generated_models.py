from django.core.management.base import BaseCommand
from django.core.management import call_command
from pathlib import Path
import os

class Command(BaseCommand):
    help = 'Delete generated_models.py and reset the database'

    def handle(self, *args, **kwargs):
        # مسیر فایل generated_models.py
        generated_models_path = Path('core') / 'generated_models.py'

        # حذف فایل generated_models.py اگر وجود داشته باشد
        if generated_models_path.exists():
            generated_models_path.unlink()
            self.stdout.write(self.style.SUCCESS('Deleted core/generated_models.py'))
        else:
            self.stdout.write(self.style.WARNING('core/generated_models.py does not exist'))

        # اجرای دستور reset_database
        self.stdout.write('Running reset_database...')
        call_command('reset_database', verbosity=1)

        self.stdout.write(self.style.SUCCESS('Generated models deleted and database reset successfully'))