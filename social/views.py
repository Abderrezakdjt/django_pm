from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Friendship, Message, Notification
from .forms import MessageForm

@login_required
def friend_list(request):
    """عرض قائمة الأصدقاء"""
    friends = User.objects.filter(
        Q(sent_friend_requests__to_user=request.user, sent_friend_requests__status='accepted') |
        Q(received_friend_requests__from_user=request.user, received_friend_requests__status='accepted')
    ).distinct()
    
    return render(request, 'social/friend_list.html', {'friends': friends})

@login_required
def send_friend_request(request, user_id):
    """إرسال طلب صداقة"""
    if request.method == 'POST':
        to_user = get_object_or_404(User, id=user_id)
        
        if to_user == request.user:
            return JsonResponse({'error': 'لا يمكنك إضافة نفسك كصديق'}, status=400)
        
        # التحقق من وجود طلب مسبق
        existing_request = Friendship.objects.filter(
            Q(from_user=request.user, to_user=to_user) |
            Q(from_user=to_user, to_user=request.user)
        ).first()
        
        if existing_request:
            if existing_request.status == 'accepted':
                return JsonResponse({'error': 'أنتما بالفعل أصدقاء'}, status=400)
            return JsonResponse({'error': 'طلب صداقة موجود بالفعل'}, status=400)
        
        friendship = Friendship.objects.create(from_user=request.user, to_user=to_user)
        
        # إنشاء إشعار
        Notification.objects.create(
            user=to_user,
            from_user=request.user,
            notification_type='friend_request',
            content=f'{request.user.username} أرسل لك طلب صداقة'
        )
        
        return JsonResponse({'success': 'تم إرسال طلب الصداقة'})
    
    return JsonResponse({'error': 'طريقة غير صحيحة'}, status=405)

@login_required
def accept_friend_request(request, request_id):
    """قبول طلب صداقة"""
    if request.method == 'POST':
        friendship = get_object_or_404(Friendship, id=request_id, to_user=request.user)
        friendship.status = 'accepted'
        friendship.save()
        
        # إنشاء إشعار للطرف الآخر
        Notification.objects.create(
            user=friendship.from_user,
            from_user=request.user,
            notification_type='friend_accept',
            content=f'{request.user.username} قبل طلب صداقتك'
        )
        
        return JsonResponse({'success': 'تم قبول طلب الصداقة'})
    
    return JsonResponse({'error': 'طريقة غير صحيحة'}, status=405)

@login_required
def reject_friend_request(request, request_id):
    """رفض طلب صداقة"""
    if request.method == 'POST':
        friendship = get_object_or_404(Friendship, id=request_id, to_user=request.user)
        friendship.delete()
        return JsonResponse({'success': 'تم رفض طلب الصداقة'})
    
    return JsonResponse({'error': 'طريقة غير صحيحة'}, status=405)

@login_required
def chat_messages(request, user_id):
    """عرض محادثة مع صديق"""
    friend = get_object_or_404(User, id=user_id)
    
    # التحقق من الصداقة
    is_friend = Friendship.objects.filter(
        Q(from_user=request.user, to_user=friend, status='accepted') |
        Q(from_user=friend, to_user=request.user, status='accepted')
    ).exists()
    
    if not is_friend:
        return redirect('social:friend_list')  # تغيير هنا
    
    messages = Message.objects.filter(
        Q(sender=request.user, receiver=friend) |
        Q(sender=friend, receiver=request.user)
    )
    
    # تحديث حالة القراءة
    messages.filter(receiver=request.user, is_read=False).update(is_read=True)
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = friend
            message.save()
            
            # إشعار للمستلم
            Notification.objects.create(
                user=friend,
                from_user=request.user,
                notification_type='new_message',
                content=f'رسالة جديدة من {request.user.username}'
            )
            
            return redirect('social:chat_messages', user_id=friend.id)  # تغيير هنا
    else:
        form = MessageForm()
    
    context = {
        'friend': friend,
        'messages': messages,
        'form': form
    }
    return render(request, 'social/chat.html', context)

@login_required
def friend_requests(request):
    """عرض طلبات الصداقة الواردة"""
    pending_requests = Friendship.objects.filter(to_user=request.user, status='pending')
    return render(request, 'social/friend_requests.html', {'pending_requests': pending_requests})

@login_required
def search_users(request):
    """البحث عن مستخدمين لإضافتهم كأصدقاء"""
    query = request.GET.get('q', '')
    if query:
        users = User.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        ).exclude(id=request.user.id)
        
        # إضافة حالة الصداقة لكل مستخدم
        for user in users:
            friendship = Friendship.objects.filter(
                Q(from_user=request.user, to_user=user) |
                Q(from_user=user, to_user=request.user)
            ).first()
            if friendship:
                user.friend_status = friendship.status
            else:
                user.friend_status = 'none'
    else:
        users = []
    
    return render(request, 'social/search_users.html', {'users': users, 'query': query})

@login_required
def notifications(request):
    """عرض الإشعارات"""
    user_notifications = Notification.objects.filter(user=request.user, is_read=False)
    return render(request, 'social/notifications.html', {'notifications': user_notifications})

@login_required
def mark_notification_read(request, notification_id):
    """تحديد إشعار كمقروء"""
    if request.method == 'POST':
        notification = get_object_or_404(Notification, id=notification_id, user=request.user)
        notification.is_read = True
        notification.save()
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'طريقة غير صحيحة'}, status=405)