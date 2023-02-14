import os

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from apps.customer.services import create_customer


class Command(BaseCommand):
    help = "Add base users (for prod & dev)"
    user_model = get_user_model()

    def handle(self, *args, **options):
        self.create_admin()
        self.create_customers()

    def create_admin(self):
        user = self.user_model(username="admin", is_staff=True, is_superuser=True)
        user.set_password(os.environ.get("ADMIN_PASSWORD", "admin"))
        user.save()

    def create_customers(self):
        create_customer("Zayd")
        create_customer("Bakr")
