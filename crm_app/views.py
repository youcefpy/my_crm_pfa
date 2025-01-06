from django.shortcuts import render,redirect
from django.views import generic
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm
from .models import Lead,Agent,Client
from .forms import LeadForm,CustomUserCreationForm,AgentForm
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import send_mail


# Create your views here.



########## index page view #######

def is_super_user(user):
    return user.is_superuser

class SignupView(generic.CreateView):
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return "/login/"

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def index(request):
    if request.user.is_superuser:
        leads = Lead.objects.all()
    else :
        try:
            agent = request.user.agent
            leads = Lead.objects.filter(agent=agent)
        except : 
            print("Erreur!")
    context = {
        'leads':leads
    }
    return render(request,'index.html',context)


########## create lead view #######
@login_required
def creat_lead(request):
    '''
        Dans cette fonction create_lead cree prospet on commance par verifier si l'utilisateur est admin. si il est admin il peut cree des leads et ajouter des agent. si l'utilisateur n;est pas admin alors le champ agent <- l'utilisateur connecté.
    '''
    if request.method == "POST":
        if request.user.is_superuser:
            form = LeadForm(request.POST,request.FILES)
        else :
            form = LeadForm(request.POST,request.FILES,exclude_agent=True)

        if form.is_valid():
            lead = form.save(commit=False) # commit = Fasle c-a-d que je ne doit pas sauvgarde dans la db
            if not request.user.is_superuser:
                # si user n'est pas admin alors le champ agent recoit request.user.agent
                lead.agent = request.user.agent
            lead.save() # sauvgarde dans la db avec verification
            return redirect('index')
    else :
        if request.user.is_superuser :
            form = LeadForm()
        else : 
            form = LeadForm(exclude_agent=True)
    
    context = {
        'form':form

    }
    return render(request,'leads/create_lead.html',context)


################### Update load view #############################
@login_required
def update_lead(request,pk):
    lead = Lead.objects.get(id=pk)
    form = LeadForm(instance=lead)
    if request.method=="POST":
        if request.user.is_superuser:
            form = LeadForm(request.POST,request.FILES,instance=lead)
        else : 
            form = LeadForm(request.POST,request.FILES,instance=lead,exclude_agent=True)
        if form.is_valid():
            lead = form.save(commit=False)
            if not request.user.is_superuser:
                lead.agent = request.user.agent
            lead.save()
            return redirect('index')
    else:
        if request.user.is_superuser:
            form = LeadForm(instance=lead)
        else:
            form = LeadForm(instance=lead, exclude_agent=True)
    context = {
        'lead':lead,
        'form' : form
    }
    return render(request,'leads/update_lead.html',context )


############## Delete Lead View #####################
@login_required
def delete_lead(request,pk):

    lead = Lead.objects.get(id=pk)
    lead.delete()

    return redirect('index')



########## details leads view #######
@login_required
def details(request,pk):
    get_lead = Lead.objects.get(id=pk)
    context = {
        'get_lead':get_lead,
    }
    return render(request,'leads/details_lead.html',context)


########## create agent  view #######
@user_passes_test(is_super_user)
def create_agent(request):
    if request.method == 'POST':
        form = AgentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = AgentForm()  
    context = {
        'form' :form
    }
    return render(request,'agents/create_agent.html',context)


########### List of agents #############
@user_passes_test(is_super_user)
def list_agents(request) : 
    agents = Agent.objects.all()

    context={
        'agents':agents
    }
    return render(request,'agents/list_agents.html',context)

################ Logic of sending an email for each user #######################
@login_required
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
    return render(request,'leads/send_email.html',context)


####################### CREATION DE CLINET ################################

def create_client(request,pk):
    """
    On cree un client a partir d'un lead (prospet).
    Apres contact de l'agent avec le prospet. le prospet accepte d'acheté le produit ou la transaction. le client va ajouté le prospet a la liste des clients
    
    pour faire ca il nous faut d'abord recuperer le prospet (id).
    on cree le client. 

    le prospet doit etre supprimer de la table Lead et ajouter a la table Client

    """
    lead = Lead.objects.get(id=pk)
    if lead.is_client:
        return redirect('list_client')

    lead.is_client = True
    lead.save()

    #creation d'un client basé sur le lead
    Client.objects.create(lead=lead)
    
    return redirect('list_client')

########## List Client ###########

def list_client(request):
    if request.user.is_superuser:
        clients = Client.objects.all()
    else : 
        agent = request.user.agent 
        clients = Client.objects.filter(lead__agent = agent)

    context = {
        'clients':clients
    }

    return render(request,'clients/list_clients.html',context)