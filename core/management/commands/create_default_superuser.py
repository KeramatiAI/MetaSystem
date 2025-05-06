from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

class Command(BaseCommand):
    help = 'Create a default superuser if it does not exist'

    def handle(self, *args, **kwargs):
        default_username = 'admin'
        default_email = 'admin@example.com'
        default_password = 'admin123'

        try:
            # بررسی وجود سوپریوزر
            if not User.objects.filter(username=default_username).exists():
                # ایجاد سوپریوزر
                User.objects.create_superuser(
                    username=default_username,
                    email=default_email,
                    password=default_password
                )
                self.stdout.write(self.style.SUCCESS(
                    f'Superuser created successfully: username={default_username}, password={default_password}'
                ))
            else:
                self.stdout.write(self.style.WARNING(
                    f'Superuser with username "{default_username}" already exists'
                ))
        except IntegrityError:
            self.stdout.write(self.style.ERROR(
                'Error creating superuser due to database integrity issues'
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f'Error creating superuser: {str(e)}'
            ))