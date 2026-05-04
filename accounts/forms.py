from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordChangeForm
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from .models import UserProfile 

attrs = {'class': 'form-control'}

class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')

    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update(attrs=attrs)
        self.fields['new_password1'].widget.attrs.update(attrs=attrs)
        self.fields['new_password2'].widget.attrs.update(attrs=attrs)



class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(
        label=_('Username'),
        widget=forms.TextInput(attrs={'class': 'form-control'})  
    )
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={'class': 'form-control'})  
    )


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(
        label=_('First Name'),
        widget=forms.TextInput(attrs={'class': 'form-control'})  
    )
    last_name = forms.CharField(
        label=_('Last Name'),
        widget=forms.TextInput(attrs={'class': 'form-control'})  # تأكد من إضافة الصفات هنا
    )
    username = forms.CharField(
        label=_('Username'),
        widget=forms.TextInput(attrs={'class': 'form-control'})  # تأكد من إضافة الصفات هنا
    )
    email = forms.EmailField(
        label=_('Email'),
        widget=forms.TextInput(attrs={'class': 'form-control'})  # تأكد من إضافة الصفات هنا
    )
    password1 = forms.CharField(
        label=_('Password'),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})  # تأكد من إضافة الصفات هنا
    )
    password2 = forms.CharField(
        label=_('Password Confirmation'),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})  # تأكد من إضافة الصفات هنا
    )

    organization_name = forms.CharField(
        label=_('Organization Name'),
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    location = forms.CharField(
        label=_('Location'),
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    phone_number = forms.CharField(
        label=_('Phone Number'),
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    birthday = forms.DateField(
        label=_('Birthday'),
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})  # تأكد من إضافة الصفات هنا
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', 
                  'organization_name', 'location', 'phone_number', 'birthday')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            
            profile = user.userprofile
            if profile:
                profile.organization_name = self.cleaned_data['organization_name']
                profile.location = self.cleaned_data['location']
                profile.phone_number = self.cleaned_data['phone_number']
                profile.birthday = self.cleaned_data['birthday']
                if 'profile_picture' in self.cleaned_data:
                    profile.profile_picture = self.cleaned_data['profile_picture']
                profile.save()
        return user


    def delete_user(self):
        if self.instance.username == self.cleaned_data['username']:
            self.instance.delete()
            return True
        return False





class ProfileForm(UserChangeForm):
    password = None
    
    organization_name = forms.CharField(
        label=_('Organization Name'),
        required=False,
        widget=forms.TextInput()
    )
    location = forms.CharField(
        label=_('Location'),
        required=False,
        widget=forms.TextInput()
    )
    phone_number = forms.CharField(
        label=_('Phone Number'),
        required=False,
        widget=forms.TextInput()
    )
    birthday = forms.DateField(
        label=_('Birthday'),
        required=False,
        widget=forms.DateInput(attrs={ 'type': 'date'})
    )
    profile_picture = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput()
    )

    class Meta:
        model = User  
        fields = ['first_name', 'last_name', 'email', 'organization_name', 'location', 'phone_number', 'birthday', 'profile_picture']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()  
           
            profile = user.userprofile  
            if profile:  
                profile.organization_name = self.cleaned_data['organization_name']
                profile.location = self.cleaned_data['location']
                profile.phone_number = self.cleaned_data['phone_number']
                profile.birthday = self.cleaned_data['birthday']
                profile.profile_picture = self.cleaned_data['profile_picture']
                profile.save()  
        return user
        


    
   





