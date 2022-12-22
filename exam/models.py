from django.db import models
from student.models import Student
from django.contrib.auth.models import User

class Exam(models.Model):
   exam_name = models.CharField(max_length=50)
   question_number = models.PositiveIntegerField()
   total_marks = models.PositiveIntegerField()
   subject = models.ForeignKey('exam.Subject',on_delete=models.CASCADE)
   class_id= models.ForeignKey('exam.Class',on_delete=models.CASCADE)
   timmer = models.PositiveIntegerField()
   teacher = models.ForeignKey('teacher.Teacher',on_delete=models.CASCADE)
   visiable = models.BooleanField(default=False) 
   def __str__(self):
        return self.exam_name
                 
class multichoice_question(models.Model):
    exam=models.ForeignKey(Exam,on_delete=models.CASCADE)
    marks=models.PositiveIntegerField()
    question=models.CharField(max_length=600)
    option1=models.CharField(max_length=200)
    option2=models.CharField(max_length=200)
    option3=models.CharField(max_length=200)
    option4=models.CharField(max_length=200)
    cat=(('Option1','Option1'),('Option2','Option2'),('Option3','Option3'),('Option4','Option4'))
    answer=models.CharField(max_length=200,choices=cat)

class True_false_question(models.Model):
    exam=models.ForeignKey(Exam,on_delete=models.CASCADE)
    question=models.CharField(max_length=600)
    marks=models.PositiveIntegerField()
    answer=models.CharField(max_length=6, choices=(('True', 'True'), ('False', 'False')))

class filling_gap_question(models.Model):
    exam=models.ForeignKey(Exam,on_delete=models.CASCADE)
    question_part1=models.CharField(max_length=600)
    question_part2=models.CharField(max_length=600)
    marks=models.PositiveIntegerField()
    answer=models.CharField(max_length=30)


class Result(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam,on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)


class Announcement(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=1500)

  
    @property
    def get_name(self):
        return self.author.first_name+" "+self.author.last_name

    def __str__(self):
        return self.name



# /////////////////////////////////////////////////////////////////////////////

class Class(models.Model):
    name = models.CharField(max_length=40)
    
    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name
