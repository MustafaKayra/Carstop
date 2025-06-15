from datetime import datetime
from django.utils import timezone

def get_countdown_data(ad):
    now = timezone.now()
    remaining = ad.targetime - now

    if remaining.total_seconds() <= 0:
        return "Zaman doldu!"

    days = remaining.days
    hours, remainder = divmod(remaining.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return {
        'days': days,
        'hours': hours,
        'minutes': minutes,
        'seconds': seconds
    }