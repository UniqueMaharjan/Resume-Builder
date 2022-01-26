from django.http import HttpResponse
from django.shortcuts import redirect, render
from io import BytesIO
from django.template.loader import get_template
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .models import Education, Interests, Projects, ResumeUser, Skills, User,Experience
from .forms import EducationForm, MyUserCreationForm,ExperienceForm,ResumeUserForm,SkillForm,InterestForm,ProjectForm
from django.core.mail import send_mail
from xhtml2pdf import pisa

# Create your views here.
def Userlogin(request):
    page = 'login'
    if request.method == "POST":
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request,"User doesn't exist!!!")
       
        user = authenticate(request, email = email, password = password)
        if user != None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Email or Password doesn't exist!!")

    content = {'page':page}
    return render(request,'resumeapp/login.html',content)

def Userlogout(request):
    logout(request)
    return redirect('home')

def RegisterUser(request):
    form = MyUserCreationForm()
    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.email.lower()
            user.save()
            messages.success(request,'Successfully User Created!!')
            return redirect ('login')
            
        else:
            messages.error(request," Both Password doesn't match")
    content = {}
    return render(request,'resumeapp/login.html',content)

def home(request):
    content = {}
    return render(request,'resumeapp/home.html',content)

def ResumeTemp(request):
    content = {}
    return render(request,'resumeapp/temp.html',content)

def ContactUs(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        subject = request.POST.get('subject')
        data = {
            'name':name,
            'email':email,
            'message':message,
            'subject':subject
        }
        message = '''
            New message: {}

            From: {}
        '''.format(data['message'],data['email'])
        send_mail(data['subject'],message,'',['test.reply77@gmail.com'])
    content = {}
    return render(request,'resumeapp/contactus.html',content)

def TemplateO(request):
    return render(request,'resumeapp/template1.html')


def EntryInfo(request):
    page = 'create-info'
    if request.method == "POST":
        full_name = request.POST.get("name")
        email = request.POST.get("email")
        phone_no = request.POST.get("phone")
        role = request.POST.get("role")
        bio = request.POST.get("bio")
        skills = request.POST.get("skill")
        interest = request.POST.get("interest")
        resume = ResumeUser.objects.create(
            host = request.user,
            name = full_name,
            email = email,
            phone_no = phone_no,
            developer_role = role,
            bio = bio
        )
        Skills.objects.create(
            person = resume,
            skill = skills
        )
       
        Interests.objects.create(
            person = resume,
            interest = interest
        )
        messages.success(request,'Creation was SuccessFull!!!')
        return redirect('create')
        
    content = {'page':page}
    return render(request,'resumeapp/create-form.html',content)

def Information(request):
    page = 'info'
    try:
        resumeuser = ResumeUser.objects.filter(host = request.user).last()
        skills = Skills.objects.get(person = resumeuser)
        interest = Interests.objects.get(person = resumeuser)
    except:
        messages.error(request,'There is no any saved information to view!!')
        return redirect('create')
    return render(request,'resumeapp/create-form.html',{'user':resumeuser,'skill':skills,'interest':interest,'page':page})


def EditSkill(request):
    resumeuser = ResumeUser.objects.filter(host = request.user).last()
    skills = Skills.objects.get(person = resumeuser)
    skill_form = SkillForm(instance=skills)
    if request.method =="POST":
        skill_form = SkillForm(request.POST,instance = skills)
        skill_form.save()
        messages.success(request,'Information Updated Success Fully')
        return redirect('info')
    return render(request,'resumeapp/create-form.html',{'form1':skill_form})

def EditInterest(request):
    resumeuser = ResumeUser.objects.filter(host = request.user).last()
    interest = Interests.objects.get(person = resumeuser)
    interest_form = InterestForm(instance = interest)
    if request.method =="POST":
        interest_form = InterestForm(request.POST,instance = interest)
        interest_form.save()
        messages.success(request,'Information Updated Success Fully')
        return redirect('info')
    return render(request,'resumeapp/create-form.html',{'form1':interest_form})



def ResumeGenerate(request):
    page = 'generate'
    resumeuser = ResumeUser.objects.filter(host = request.user).last()
    if resumeuser != None:
        experience = Experience.objects.filter(worker = resumeuser)
        education = Education.objects.filter(student = resumeuser)
        project = Projects.objects.filter(owner = resumeuser)
        skill = Skills.objects.get(person = resumeuser)
        interest = Interests.objects.get(person = resumeuser)
        

    else:
        return redirect('template1')
    content = {
        'page':page,
        'resume':resumeuser,
        'skill':skill,
        'interest':interest,
        'experience':experience,
        'education':education,
        'project':project,
    }
    
    return render(request,'resumeapp/template1.html',content)


def experience(request):
    resumeuser = ResumeUser.objects.filter(host = request.user).last()
    exp = Experience.objects.filter(worker = resumeuser)
    content = {'exp':exp}
    return render(request,'resumeapp/experience.html',content)

def EntryExperience(request):
    page = "exp"
    if request.method == "POST":
        company_name = request.POST.get('company_name')
        location = request.POST.get('company_location')
        role = request.POST.get('role_in_company')
        from_date = request.POST.get('join_date')
        to_date = request.POST.get('leave_date')
        resumeuser = ResumeUser.objects.filter(host=request.user).last()
        Experience.objects.create(
            worker = resumeuser,
            company_name = company_name,
            company_location = location,
            role_in_company = role,
            join_date = from_date,
            leave_date = to_date
        )
        return redirect('experience')
    return render(request,'resumeapp/exp_creator.html',{'page':page})

def EditExperience(request,pk):
    exp = Experience.objects.get(id = pk)
    form = ExperienceForm(instance=exp)
    if request.method == "POST":
        form = ExperienceForm(request.POST,instance = exp)
        if form.is_valid():
            form.save()
            return redirect('experience')
    
    return render(request,'resumeapp/exp_creator.html',{'form':form})

def DeleteExperience(request,pk):
    exp = Experience.objects.get(id = pk)
    exp.delete()
    messages.success(request,'Deleted SuccessFully !!')
    return redirect('experience')

def education(request):
    resumeuser = ResumeUser.objects.filter(host = request.user).last()
    edu = Education.objects.filter(student =resumeuser)
    content = {'edu':edu}
    return render(request,'resumeapp/education.html',content)

def EntryEducation(request):
    page = "edu"
    if request.method == "POST":
        college_name = request.POST.get('college_name')
        college_location = request.POST.get('college_location')
        join_date = request.POST.get('join_date')
        leave_date = request.POST.get('leave_date')
        resumeuser = ResumeUser.objects.filter(host = request.user).last()
        Education.objects.create(
            student = resumeuser,
            college_name = college_name,
            college_location = college_location,
            join_date = join_date,
            leave_date = leave_date 
        )
        return redirect('education')
    content = {
        'page':page,
    }
    return render(request,'resumeapp/edu-creator.html',content)

def EditEducation(request,pk):
    education = Education.objects.get(id = pk)
    form = EducationForm(instance=education)
    if request.method == "POST":
        form = EducationForm(request.POST,instance = education)
        if form.is_valid():
            form.save()
            messages.success(request,'Education Updated Successfully')
            return redirect('education')
        else:
            messages.error(request,'Error while updating value!!')
    return render(request,'resumeapp/edu-creator.html',{'form':form})

def DeleteEducation(request,pk):
    edu = Education.objects.get(id = pk)
    edu.delete()
    messages.success(request,'Deleted Successfully!!')
    return redirect('education')

def Project(request):
    resumeuser = ResumeUser.objects.filter(host = request.user).last()
    project = Projects.objects.filter(owner = resumeuser)
    content = {'project':project}
    return render(request,'resumeapp/projects.html',content)

def EntryProject(request):
    page = "project"
    resumeuser = ResumeUser.objects.filter(host = request.user).last()
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        Projects.objects.create(
            owner = resumeuser,
            title = title,
            description = description
        )
        messages.success(request,'Project added!!')
        return redirect('project')
    
    return render(request,'resumeapp/project-creator.html',{'page':page})

def EditProject(request,pk):
    project = Projects.objects.get(id = pk)
    form = ProjectForm(instance=project)
    if request.method == "POST":
        form = ProjectForm(request.POST,instance=project)
        if form.is_valid():
            form.save()
            messages.success(request,'Project updated !!')
            return redirect ('project')
    
    return render(request,'resumeapp/project-creator.html',{'form':form})

def DeleteProject(request,pk):
    project = Projects.objects.get(id = pk)
    project.delete()
    messages.success(request,'Deleted Successfully')
    return redirect('project')

def pdf_report_create(request):
    resumeuser = ResumeUser.objects.filter(host = request.user).last()
    experience = Experience.objects.filter(worker = resumeuser)
    education = Education.objects.filter(student = resumeuser)
    project = Projects.objects.filter(owner = resumeuser)
    skill = Skills.objects.get(person = resumeuser)
    interest = Interests.objects.get(person = resumeuser)
    template_path = 'resumeapp/pdf_template.html'
    context = {
        'resume':resumeuser,
        'skill':skill,
        'interest':interest,
        'experience':experience,
        'education':education,
        'project':project,
    }
    
    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'filename="Resume.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response