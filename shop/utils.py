from datetime import datetime
from django.utils import timezone
from .models import Bid
from django.core.mail import send_mail
from django.conf import settings

def get_countdown_data(ad):
    now = timezone.now()
    remaining = ad.targetime - now

    if remaining.total_seconds() <= 0 and ad.is_active == True:
        top_bid = Bid.objects.filter(ad=ad).order_by('-amount').first()
        print(top_bid)
        print(f"Teklif Yapan Kullanıcı: {top_bid.user.email}")
    
        if top_bid:
            send_mail(
                subject="Tebrikler! Teklifiniz Kazandı",
                message=f"{ad.adname} ilanına verdiğiniz {top_bid.amount} TL'lik teklif kazandı!",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[top_bid.user.email],
                fail_silently=False,
            )
        else:
            print("Hiç Teklif Yapılmamış")

        ad.is_active = False
        ad.save(update_fields=['is_active'])
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