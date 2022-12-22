from django.db import models
from django.contrib.auth.models import User




class Student(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    class_id = models.ForeignKey('exam.Class',on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic/Student/',null=True,blank=True)
    phone_number = models.CharField(max_length=10,null=False) 
    status= models.BooleanField(default=False)


    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name

    @property
    def get_email(self):
        return self.user.email
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.user.first_name