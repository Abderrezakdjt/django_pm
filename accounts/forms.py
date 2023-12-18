from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


# Common attributes for form fields
attrs = {'class': 'form-control'}


# User Login Form
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs=attrs)
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs=attrs)
    )


# User Registration Form
class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(
        label='First_Name',
        widget=forms.TextInput(attrs=attrs)
    )
    last_name = forms.CharField(
        label='Last_Name',
        widget=forms.TextInput(attrs=attrs)
    )
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs=attrs)
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.TextInput(attrs=attrs),
        help_text='Enter your email address',
    )
    password1 = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs=attrs)
    )
    password2 = forms.CharField(
        label='Password Confirmation',
        strip=False,
        widget=forms.PasswordInput(attrs=attrs)
    )
    birthday = forms.DateField(
        label='Birthday',
        widget=forms.DateInput({'class': 'form-control', 'placeholder': 'DD/MM/YYYY'}, format='%d/%m/%Y' ),
        input_formats=['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y', '%Y/%m/%d', '%d/%m/%Y'],
    )

    class Meta(UserCreationForm.Meta):
        fields = ('first_name', 'last_name', 'birthday', 'username', 'email')


class ProfileForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput({'class': 'form-control', 'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput({'class': 'form-control', 'placeholder': 'Enter your last name'}),
            'email': forms.EmailInput({'class': 'form-control', 'placeholder': 'Enter your email address'}),
        }






