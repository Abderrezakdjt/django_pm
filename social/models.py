from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Friendship(models.Model):
    """نموذج الصداقة بين مستخدمين"""
    STATUS_CHOICES = [
        ('pending', 'قيد الانتظار'),
        ('accepted', 'مقبولة'),
        ('rejected', 'مرفوضة'),
        ('blocked', 'محظور'),
    ]
    
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_friend_requests')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_friend_requests')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['from_user', 'to_user']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.from_user} -> {self.to_user}: {self.status}"

class Message(models.Model):
    """نموذج الرسائل بين الأصدقاء"""
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.sender} to {self.receiver}: {self.content[:50]}"
    
    def mark_as_read(self):
        self.is_read = True
        self.save()

class Notification(models.Model):
    """نموذج الإشعارات"""
    NOTIFICATION_TYPES = [
        ('friend_request', 'طلب صداقة'),
        ('friend_accept', 'قبول صداقة'),
        ('new_message', 'رسالة جديدة'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications', null=True, blank=True)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user}: {self.content[:50]}"