from django.forms import ModelForm
from .models import Experience,Education, Interests, Projects, Skills,User,ResumeUser
from django.contrib.auth.forms import UserCreationForm

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name','username','email','password1','password2']

class ResumeUserForm(ModelForm):
    class Meta:
        model = ResumeUser
        exclude = ['host']

class SkillForm(ModelForm):
    class Meta:
        model = Skills
        exclude = ['person']

class InterestForm(ModelForm):
    class Meta:
        model = Interests
        exclude = ['person']

class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        exclude = ['worker']

class EducationForm(ModelForm):
    class Meta:
        model = Education
        exclude = ['student']


class ProjectForm(ModelForm):
    class Meta:
        model = Projects
        exclude = ['owner']