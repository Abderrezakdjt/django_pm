from django.contrib.auth.views import LoginView
from django.urls import path, include
from accounts.forms import UserLoginForm
from accounts.views import RegisterView, edit_profile, delete_account, change_password
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login/', LoginView.as_view(authentication_form=UserLoginForm), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', edit_profile, name='profile'),
    path('delete_account/', delete_account, name='delete_account'),
    path('change_password/', change_password, name='change_password'),
    path('', include('django.contrib.auth.urls'))
]








