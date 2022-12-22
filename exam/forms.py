from django import forms
from django.contrib.auth.models import User
from . import models
from teacher import models as TMODEL

class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))
    
class TeacherSalaryForm(forms.Form):
    salary=forms.IntegerField()

class ExamForm(forms.ModelForm):
    subjectID = forms.ModelChoiceField(queryset=models.Subject.objects.all(),empty_label="Subject", to_field_name="id")
    classID = forms.ModelChoiceField(queryset=models.Class.objects.all(),empty_label="Class", to_field_name="id")
    class Meta:
        model=models.Exam
        fields=['exam_name','question_number','total_marks','timmer']

class QuestionForm_multichoice(forms.ModelForm):
    
    #this will show dropdown __str__ method exam model is shown on html so override it
    #to_field_name this will fetch corresponding value  user_id present in exam model and return it
    examID=forms.ModelChoiceField(queryset=models.Exam.objects.all(),empty_label="Exam Name", to_field_name="id")
    class Meta:
        model=models.multichoice_question
        fields=['marks','question','option1','option2','option3','option4','answer']
        widgets = {
            'question': forms.Textarea(attrs={'rows': 3, 'cols': 50})
        }

class Truefalse(forms.ModelForm):

    examID=forms.ModelChoiceField(queryset=models.Exam.objects.all(),empty_label="Exam Name", to_field_name="id")
    class Meta:
        model=models.True_false_question
        fields=['question', 'marks',  'answer']
        widgets = {
            'question': forms.Textarea(attrs={'rows': 3, 'cols': 50})
        }

class Gapfilling(forms.ModelForm):

    examID=forms.ModelChoiceField(queryset=models.Exam.objects.all(),empty_label="Exam Name", to_field_name="id")
    class Meta:
        model=models.filling_gap_question
        fields=['question_part1', 'question_part2', 'marks',  'answer']
        widgets = {
            'question_part1': forms.Textarea(attrs={'rows': 3, 'cols': 50}),
            'question_part2': forms.Textarea(attrs={'rows': 3, 'cols': 50})
        }


class Announcement(forms.ModelForm):
    class Meta:
        model=models.Announcement
        fields=['title', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 10, 'cols': 50})
        }

class OTPasswordChange(forms.Form):
    password1 = forms.CharField(max_length=30)
    password2 = forms.CharField(max_length=30)
