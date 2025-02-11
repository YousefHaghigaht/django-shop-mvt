from celery import shared_task
from datetime import datetime,timedelta
import pytz
from .models import OtpCode

@shared_task
def remove_expired_codes():
    expire_time = datetime.now(tz=pytz.timezone('Asia/Tehran')) - timedelta(minutes=1)
    OtpCode.objects.filter(created__lt=expire_time).delete()
