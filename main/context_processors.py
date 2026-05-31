
from .models import BuyRequest

def seller_notification_count(request):

    if request.session.get('user_id'):

        seller_id = request.session.get('user_id')

        pending_requests = BuyRequest.objects.filter(
            waste__seller_id=seller_id,
            status='Pending'
        ).count()

        return {
            'pending_requests_count': pending_requests
        }

    return {
        'pending_requests_count': 0
    }

