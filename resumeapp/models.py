from passlib.hash import pbkdf2_sha256
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
# Create your models here.

def phone_no_valid(value):
    if len(value) == 14:
        return value
    else:
        raise ValidationError("Please Enter Valid Phone number.")

def email_valid(value):
    if '@gmail.com' in value:
        return value
    else:
        raise ValidationError("Please use google mail only")

class User(AbstractUser):
    name = models.CharField(max_length=150,null=True)
    email = models.EmailField(unique=True, validators=[email_valid],null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def verify_password(self,raw_password):
        return pbkdf2_sha256.verify(raw_password,self.password)

class ResumeUser(models.Model):
    host = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200,null=True,blank=True)
    email = models.CharField(max_length=100,null=True,blank=True)
    phone_no = models.CharField(max_length=14, validators=[phone_no_valid],null=True,blank=True)
    developer_role = models.CharField(max_length=200, null = True,blank=True)
    bio = models.TextField(null=True,blank=True)
    created = models.DateTimeField(auto_now_add = True)
    
    class Meta:
        get_latest_by = "created"
    
    def __str__(self):
        return self.name

class Experience(models.Model):
    worker = models.ForeignKey(ResumeUser,on_delete=models.CASCADE,null=True)
    company_name = models.CharField(max_length=250,null=True,blank=True)
    company_location = models.CharField(max_length=200,null=True,blank=True)
    role_in_company = models.CharField(max_length=150,null=True,blank=True)
    join_date = models.DateField(null=True,blank=True)
    leave_date = models.DateField(null = True,blank=True)

    def __str__(self):
        return self.worker.name

class Education(models.Model):
    student = models.ForeignKey(ResumeUser,on_delete=models.CASCADE,null=True)
    college_name = models.CharField(max_length=200,null=True,blank=True)
    college_location = models.CharField(max_length=200,null=True,blank=True)
    join_date = models.DateField(null=True,blank=True)
    leave_date = models.DateField(null=True,blank=True)

    def __str__(self):
        return self.student.name

class Projects(models.Model):
    owner = models.ForeignKey(ResumeUser,on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=100,null=True)
    description = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.owner.name

class Skills(models.Model):
    person = models.ForeignKey(ResumeUser,on_delete=models.CASCADE,null=True)
    skill = models.CharField(max_length=50,null=True,blank=True)

    def __str__(self):
        return self.person.name

class Interests(models.Model):
    person = models.ForeignKey(ResumeUser,on_delete=models.CASCADE,null=True)
    interest = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.person.name
    