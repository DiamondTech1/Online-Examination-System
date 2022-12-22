from django.db import models
from django.contrib.auth.models import User


class Teacher(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    subject = models.ForeignKey('exam.Subject',on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/Teacher/',null=True,blank=True)
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