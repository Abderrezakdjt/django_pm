from django.urls import reverse_lazy
from django.views.generic import CreateView
from accounts.forms import UserRegisterForm, ProfileForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import DeleteAccountForm
from .forms import CustomPasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
# from django.views.decorators.http import require_POST
# from django.contrib.auth.views import LogoutView


@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
    else:
        form = CustomPasswordChangeForm(request.user)

    return render(request, 'change_password.html', {'form': form})


def delete_account(request):
    if request.method == 'POST':
        form = DeleteAccountForm(request.POST)
        if form.is_valid() and form.cleaned_data[_("confirmation")]:
            request.user.delete()
            return redirect('logout')

    else:
        form = DeleteAccountForm()
    return render(request, 'delete_account.html', {'form': form})


class RegisterView(CreateView):
    form_class = UserRegisterForm
    # success_url = reverse_lazy('login')
    template_name = 'registration/register.html'

    def get_success_url(self):
        login(self.request, self.object)
        return reverse_lazy('Project_list')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Error updating profile. Please check the form.')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
        return render(request, 'profile.html', {
            'form': form
        })





