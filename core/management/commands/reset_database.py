from django.core.management.base import BaseCommand
from django.core.management import call_command
import os
from pathlib import Path
from core.models import Entity, Field


class Command(BaseCommand):
    help = 'Reset database, reapply migrations, ensure migrations __init__.py exists, and add initial data'

    def handle(self, *args, **kwargs):
        # مسیر دیتابیس
        db_path = Path('db.sqlite3')

        # حذف دیتابیس
        if db_path.exists():
            os.remove(db_path)
            self.stdout.write(self.style.SUCCESS('Database deleted.'))

        # مسیر پوشه migrations
        migrations_path = Path('core/migrations')

        # اطمینان از وجود پوشه migrations
        migrations_path.mkdir(parents=True, exist_ok=True)

        # بررسی و ایجاد __init__.py
        init_file = migrations_path / '__init__.py'
        if not init_file.exists():
            init_file.touch()
            self.stdout.write(self.style.SUCCESS('Created core/migrations/__init__.py'))

        # حذف فایل‌های مهاجرت قدیمی (به جز __init__.py)
        for item in migrations_path.glob('*.py'):
            if item.name != '__init__.py':
                item.unlink()
        self.stdout.write(self.style.SUCCESS('Migration files deleted.'))

        # ساخت و اعمال مهاجرت‌ها
        self.stdout.write('Creating migrations...')
        call_command('makemigrations', verbosity=1)
        self.stdout.write('Applying migrations...')
        call_command('migrate', verbosity=1)

        # اضافه کردن داده‌های اولیه
        self.stdout.write('Adding initial data...')
        user_entity, _ = Entity.objects.get_or_create(name='User')
        Field.objects.get_or_create(
            entity=user_entity,
            name='username',
            field_type='char',
            is_required=True,
            max_length=100
        )
        Field.objects.get_or_create(
            entity=user_entity,
            name='age',
            field_type='int',
            is_required=False
        )
        order_entity, _ = Entity.objects.get_or_create(name='Order')
        Field.objects.get_or_create(
            entity=order_entity,
            name='order',
            field_type='char',
            is_required=True
        )
        self.stdout.write(self.style.SUCCESS('Initial data added.'))

        self.stdout.write(self.style.SUCCESS('Database reset and migrations applied successfully.'))