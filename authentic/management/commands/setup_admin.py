import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()
class Command(BaseCommand):
    help = 'Create an admin superuser - from .env DJANGO_SUPERUSER parameters'

    def handle(self, *args, **options):
        user = User.objects.filter(username=os.getenv('DJANGO_SUPERUSER_USERNAME','admin'))
        
        if(not user.exists()):
            User.objects.create_superuser(
                    username=os.getenv('DJANGO_SUPERUSER_USERNAME','admin'),
                    email=os.getenv('DJANGO_SUPERUSER_EMAIL','admin@mail.com'),
                    password=os.getenv('DJANGO_SUPERUSER_PASSWORD','admin123')
                    )