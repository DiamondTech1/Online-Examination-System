from django import forms
from django.contrib.auth.models import User
from . import models
from exam import models as QMODEL

class StudentUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','email','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }


class StudentForm(forms.ModelForm):
    classID=forms.ModelChoiceField(queryset=QMODEL.Class.objects.all(),empty_label="*Class Name", to_field_name="id")
    class Meta:
        model=models.Student
        fields=['phone_number','profile_pic']

class OTPasswordChange(forms.Form):
    password = forms.CharField(max_length=30)
    password1 = forms.CharField(max_length=30)


        
