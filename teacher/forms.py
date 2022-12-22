from django import forms
from django.contrib.auth.models import User
from . import models
from exam import models as QMODEL

class TeacherUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','email','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class TeacherForm(forms.ModelForm):
    subjectID=forms.ModelChoiceField(queryset=QMODEL.Subject.objects.all(),empty_label="Department", to_field_name="id")
    class Meta:
        model=models.Teacher
        fields=['phone_number','profile_pic']


class OTPasswordChange(forms.Form):
    password = forms.CharField(max_length=30)
    password1 = forms.CharField(max_length=30)


