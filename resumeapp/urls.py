from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name = 'home'),
    path('login/',views.Userlogin,name = 'login'),
    path('logout/',views.Userlogout,name = 'logout'),
    path('signin/',views.RegisterUser,name = 'register'),
    path('templates/',views.ResumeTemp, name = 'template'),
    path('demotemplate/',views.TemplateO, name = 'template1'),
    path('contactus/',views.ContactUs, name = 'contact'),
    #create resume
    path('create-form/',views.EntryInfo, name='create'),
    path('Information/',views.Information,name = 'info'),
    path('edit-skill/',views.EditSkill,name = 'edit-skill'),
    path('edit-interest/',views.EditInterest,name = 'edit-interest'),
    path('generator/',views.ResumeGenerate,name = 'generate'),
    #experience
    path('experience/',views.experience,name = "experience"),
    path('create-experience/',views.EntryExperience,name = "create-exp"),
    path('edit-experience/<int:pk>/',views.EditExperience,name = "edit-exp"),
    path('delete-experience/<int:pk>/',views.DeleteExperience,name = "delete-exp"),
    #education
    path('education/',views.education,name = 'education'),
    path('create-education/',views.EntryEducation,name = 'create-edu'),
    path('edit-education/<int:pk>/',views.EditEducation,name = 'edit-edu'),
    path('delete-education/<int:pk>/',views.DeleteEducation,name = 'delete-edu'),
    #project
    path('project/',views.Project, name = 'project'),
    path('create-project/',views.EntryProject,name = 'create-project'),
    path('edit-project/<int:pk>/',views.EditProject, name = 'edit-project'),
    path('delete-project/<int:pk>/',views.DeleteProject, name = 'delete-project'),
    #pdf convert
    path('createPdf/',views.pdf_report_create, name = "createpdf")
    ]