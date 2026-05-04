from django.db import models
from django.contrib.auth.models import User

import os
from django.utils.text import slugify
from uuid import uuid4

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    unique_filename = f"{slugify(instance.user.username)}_{uuid4()}.{ext}"
    return os.path.join('uploads/', unique_filename)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization_name = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to=get_file_path, blank=True, null=True)  # تأكد من وجود هذا السطر

    def __str__(self):
        return self.user.username

    
    def delete_profile_picture(self):
        if self.profile_picture:
             self.profile_picture.delete(save=False)  # احذف الصورة من التخزين
             self.profile_picture = None  # اضبط الحقل على None
             self.save()  # احفظ النموذج


