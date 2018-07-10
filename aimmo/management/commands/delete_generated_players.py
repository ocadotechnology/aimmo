from django.contrib.auth.models import User
from django.core.management import BaseCommand


class Command(BaseCommand):
    # Show this when the user types help
    help = "Delete generated users"

    # A command must define handle()
    def handle(self, *args, **options):
        for user in User.objects.filter(username__startswith='zombie-'):
            self.stdout.write('Deleting %s' % user.get_username())
            user.delete()
