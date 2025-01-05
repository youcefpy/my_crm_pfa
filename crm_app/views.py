from django.shortcuts import render,HttpResponse,redirect
from .models import Lead,Agent
from .forms import LeadForm,AgentForm
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import send_mail


# Create your views here.



########## index page view #######

def is_super_user(user):
    return user.is_superuser

def index(request):
    leads = Lead.objects.all()
    context = {
        'leads':leads
    }
    return render(request,'index.html',context)


########## create lead view #######
def creat_lead(request):
    if request.method == "POST":
        form = LeadForm(request.POST,request.FILES)

        if form.is_valid():
            form.save()
            return redirect('index')
    else :
        form = LeadForm()
    
    context = {
        'form':form

    }
    return render(request,'create_lead.html',context)


################### Update load view #############################

def update_lead(request,pk):
    lead = Lead.objects.get(id=pk)
    form = LeadForm(instance=lead)
    if request.method=="POST":
        form = LeadForm(request.POST,request.FILES,instance=lead)
        if form.is_valid():
            form.save()
            return redirect('index')
    context = {
        'lead':lead,
        'form' : form
    }

    return render(request,'update_lead.html',context )


############## Delete Lead View #####################

def delete_lead(request,pk):

    lead = Lead.objects.get(id=pk)
    lead.delete()

    return redirect('index')



########## details leads view #######
def details(request,pk):
    get_lead = Lead.objects.get(id=pk)
    context = {
        'get_lead':get_lead,
    }
    return render(request,'details_lead.html',context)



########## create agent  view #######
@user_passes_test(is_super_user)
def create_agent(request):
    if request.method == "POST" :
        form = AgentForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('index')
    
    else : 
        form = AgentForm()
    context = {
        'form' : form
    }
    return render(request,'create_agent.html',context)

########### List of agents #############
def list_agents(request) : 
    agents = Agent.objects.all()

    context={
        'agents':agents
    }
    return render(request,'list_agents.html',context)

################ Logic of sending an email for each user #######################

def send_email_to_lead(request,pk):
    lead= Lead.objects.get(id=pk)

    if request.method=="POST":
        #we get the value from the form 
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        from_email= 'youcefboutiche28@gmail.com'
        to_email = [lead.email]

        #sending email with send_email function 
        send_mail(subject, message, from_email, to_email)

        return redirect('details_page', lead.id)
    
    context = {
        'lead':lead,
    }
    return render(request,'send_email.html',context)