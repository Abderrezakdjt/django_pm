from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from accounts.forms import UserRegisterForm, ProfileForm
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .forms import CustomPasswordChangeForm
from django.contrib import messages
from .models import UserProfile

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  
            messages.success(request, 'Password changed successfully.')  
            return render(request, 'change_password.html', {'form': form})  
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})

class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'registration/register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)  # تسجيل دخول المستخدم بعد التسجيل
        return super().form_valid(form)

    def get_success_url(self):
        login(self.request, self.object)
        return reverse_lazy('Project_list')

@login_required
def edit_profile(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save()

            profile.organization_name = form.cleaned_data.get('organization_name')
            profile.location = form.cleaned_data.get('location')
            profile.phone_number = form.cleaned_data.get('phone_number')
            profile.birthday = form.cleaned_data.get('birthday')

            # تحقق مما إذا كانت صورة جديدة قد تم تحميلها
            if 'profile_picture' in request.FILES:
                # احذف الصورة القديمة إن وجدت
                if profile.profile_picture:
                    profile.delete_profile_picture()  # حذف الصورة القديمة

                profile.profile_picture = request.FILES['profile_picture']  # تعيين الصورة الجديدة

            if request.POST.get('delete_picture'):
                profile.delete_profile_picture()  # حذف الصورة إذا اختار المستخدم ذلك

            profile.save()
            return redirect('profile')  
    else:
        form = ProfileForm(instance=user)

    # تهيئة الحقول في النموذج
    form.fields['organization_name'].initial = profile.organization_name
    form.fields['location'].initial = profile.location
    form.fields['phone_number'].initial = profile.phone_number
    form.fields['birthday'].initial = profile.birthday

    return render(request, 'profile.html', {'form': form, 'profile': profile})

@login_required
def delete_account(request):
    if request.method == 'POST':
        if request.POST.get('confirm') == 'yes':
            request.user.delete()
            logout(request)
            return redirect('login')
        else:
            return render(request, 'delete_account.html', {'error': 'Confirmation failed.'})
    else:
        return render(request, 'delete_account.html')