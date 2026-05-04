# social/context_processors.py
from .models import Notification

def unread_notifications(request):
    """
    Context processor to add unread notifications count to all templates.
    This makes {{ unread_notifications_count }} available in every template.
    """
    if request.user.is_authenticated:
        try:
            count = Notification.objects.filter(
                user=request.user, 
                is_read=False
            ).count()
            return {'unread_notifications_count': count}
        except:
            # في حالة حدوث خطأ في قاعدة البيانات (مثلاً الجداول لم تنشأ بعد)
            return {'unread_notifications_count': 0}
    return {'unread_notifications_count': 0}