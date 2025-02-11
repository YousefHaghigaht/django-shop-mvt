from django.core.management.base import BaseCommand
from datetime import datetime,timedelta
import pytz
from accounts.models import OtpCode


class Command(BaseCommand):
    help = 'Remove all expired code'

    def handle(self, *args, **options):
        expire_time = datetime.now(tz=pytz.timezone('Asia/Tehran')) - timedelta(minutes=1)
        OtpCode.objects.filter(created__lt=expire_time).delete()
        self.stdout.write(self.style.SUCCESS('All expired codes have been removed'))
