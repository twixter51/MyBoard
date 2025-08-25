from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ...models import users, userMedia, users, userTexts  # replace with your actual model name
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Generate fake users and media records'

    def handle(self, *args, **kwargs):
        fake = Faker()
        total_users = 25

        
        #Testing
        for i in range(0, total_users):
            userTaken = users.objects.all()[i]
            userTexts.objects.create(profile=userTaken, message="Hello!")

            
        
        self.stdout.write(self.style.SUCCESS("Done generating fake data."))