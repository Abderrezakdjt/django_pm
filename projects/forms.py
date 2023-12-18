from django import forms
from . import models
from django.utils.translation import gettext_lazy as _

attrs = {'class': 'form-control ', 'id': 'disabledInput', 'type': 'text', 'placeholder': 'Disabled text here...', }


class ProjectCreateFrom(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = ['category', 'title', 'description']
        labels = {
            'category': _("category"),
            'title': _("title"),
            'description': _("description"),
        }
        widgets = {
            'category': forms.Select(attrs=attrs),
            'title': forms.TextInput(attrs=attrs),
            'description': forms.Textarea(attrs=attrs)
        }


class ProjectUpdateFrom(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = ['category', 'title', 'status']
        widgets = {
            'category': forms.Select(attrs=attrs),
            'title': forms.TextInput(attrs=attrs),
            'status': forms.Select(attrs=attrs)
        }