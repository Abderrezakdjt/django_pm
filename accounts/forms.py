from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import gettext_lazy as _
from django.contrib import messages


# Common attributes for form fields
attrs = {'class': 'form-control'}


# User Login Form
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label=_("Username"),
        widget=forms.TextInput(attrs=attrs)
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs=attrs)
    )


# User Registration Form
class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(
        label=_("First_Name"),
        widget=forms.TextInput(attrs=attrs)
    )
    last_name = forms.CharField(
        label=_("Last_Name"),
        widget=forms.TextInput(attrs=attrs)
    )
    username = forms.CharField(
        label=_("Username"),
        widget=forms.TextInput(attrs=attrs)
    )
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.TextInput(attrs=attrs),
        help_text='Enter your email address',
    )
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs=attrs)
    )
    password2 = forms.CharField(
        label=_("Password_confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs=attrs)
    )
    birthday = forms.DateField(
        label=_("Birthday"),
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


class DeleteAccountForm(forms.Form):
    confirmation = forms.BooleanField(required=True, initial=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    template_name = 'accounts/delete_account.html'


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Old Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'autocomplete': 'current-password',
        }),
    )
    new_password1 = forms.CharField(
        label=_("New Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'autocomplete': 'new-password',
        }),
        help_text=_("Enter your new password."),
    )
    new_password_confirm = forms.CharField(
        label=_("New Password Confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'autocomplete': 'new-password',
        }),
        help_text=_("Enter the same password as above, for verification."),
    )

    new_password2 = forms.CharField(
        label=_("New Password Confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'autocomplete': 'new-password',
        }),
        help_text=_("Enter the same password as above, for verification."),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_new_password_confirm(self):
        new_password = self.cleaned_data.get('new_password1')
        new_password_confirm = self.cleaned_data.get('new_password_confirm')

        if new_password and new_password_confirm and new_password != new_password_confirm:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )

        return new_password_confirm

    def save(self, commit=True):
        user = self.user
        user.set_password(self.cleaned_data['new_password1'])

        if commit:
            user.save()
            messages.success(self.request, _('Your password was successfully updated.'))

        return user





