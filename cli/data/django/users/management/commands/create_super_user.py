from django.core.management import BaseCommand
from django.db import IntegrityError


def create_super_user(
    email="admin@admin.com",
    password="admin",
    first_name="admin",
    last_name="user",
    **kwargs,
):
    from django.contrib.auth import get_user_model

    User = get_user_model()
    try:
        User.objects.create_superuser(
            email=email, password=password, first_name=first_name, last_name=last_name
        )
        print(f"user {email} created !")
    except IntegrityError as e:
        print(e)


def main(**options):
    create_super_user(**options)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--email")
        parser.add_argument("--password")
        parser.add_argument("--first_name")
        parser.add_argument("--last_name")

    def handle(self, *args, **options):
        main(**options)
