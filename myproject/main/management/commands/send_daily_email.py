from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from main.utils import send_email_notification


class Command(BaseCommand):
    help = "Send daily GameHub emails"

    def handle(self, *args, **kwargs):
        for user in User.objects.all():
            result = send_email_notification(user)

            if result == "sent":
                print(f"Email sent to {user.username}")
            elif result == "dnd":
                print(f"Email not sent to {user.username} (Do Not Disturb ON)")
            # elif result == "no_player":
            #     print(f"Skipped {user.username} (No Player)")
            # elif result == "no_email":
            #     print(f"Skipped {user.username} (No Email)")
