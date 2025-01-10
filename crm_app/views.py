from django.shortcuts import render,redirect
from django.views import generic
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm
from .models import Lead,Agent,Client,LossLead
from .forms import LeadForm,CustomUserCreationForm,AgentForm
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import send_mail
from django.db.models import Count
# from django.db.models.functions import TruncDay
from django.core.exceptions import ObjectDoesNotExist
from dashborad_app.views import (get_dashboard_data,get_prospects_by_source,get_agents_comparison,get_prospet_by_month, get_lost_lead_by_source,get_lost_prospects_by_agent,get_total_leads)

# Create your views here.


#check if the user if superuser
def is_super_user(user):
    return user.is_superuser

# check if the user is agent
def is_agent(view_func):
    """
    Vérifie si l'utilisateur est un agent. Si ce n'est pas le cas, il est redirigé.
    """
    def wrapper(request, *args, **kwargs):
        try:
            if not hasattr(request.user, 'agent'):
                return redirect('not_authorized')
        except ObjectDoesNotExist:
            return redirect('not_authorized')
        return view_func(request, *args, **kwargs)
    return wrapper

#non authorized
@login_required
def not_authorized(request):
    return render(request, 'not_authorized.html')


####################### Singup view ##################
class SignupView(generic.CreateView):
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return "/login/"
################ Logout view ################
def logout_view(request):
    logout(request)
    return redirect('login')


########## index page view #######

@login_required
@is_agent
def index(request):
    # print("Hello")
    dashboard_context = get_dashboard_data() 
    gr_get_prospects_by_source= get_prospects_by_source()
    gr_get_agents_comparison =get_agents_comparison()
    gr_get_leads_by_month = get_prospet_by_month()
    gr_get_lost_prospects_by_agent = get_lost_prospects_by_agent()
    gr_get_lost_lead_by_source = get_lost_lead_by_source()
    ge_total_leads_data = get_total_leads()

    if request.user.is_superuser:
        leads = Lead.objects.all()
    else :
        try:
            agent = request.user.agent
            leads = Lead.objects.filter(agent=agent)
        except : 
            return redirect('not_authorized')
    context = {
        'leads':leads,

        'dashboard_labels': dashboard_context['labels'],
        'dashboard_data': dashboard_context['data'],

        'prospects_by_source_labels': gr_get_prospects_by_source['labels'],
        'prospects_by_source_data': gr_get_prospects_by_source['data'],

        'lost_lead_by_source_labels': gr_get_lost_lead_by_source['labels'],
        'lost_lead_by_source_data': gr_get_lost_lead_by_source['data'],

        'agents_comparison_labels':gr_get_agents_comparison['labels'],
        'agents_comparison_data':gr_get_agents_comparison['clients_data'],
        'agents_comparison_pr_lost_dt':gr_get_agents_comparison['prospects_lost_data'],

        'get_leads_by_month_labels':gr_get_leads_by_month['labels'],
        'get_leads_by_month_data':gr_get_leads_by_month['data'],

        'lost_prospects_by_agent_labels':gr_get_lost_prospects_by_agent['labels'],
        'lost_prospects_by_agent_data':gr_get_lost_prospects_by_agent['data'],

        'total_leads_labels':ge_total_leads_data['labels'],
        'total_leads_data' : ge_total_leads_data['data']
    }
    return render(request,'index.html',context)


########## create lead view #######
@login_required
def create_lead(request):
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
            return redirect('list_leads')
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
            return redirect('list_leads')
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

############## List leads views #########################
@login_required
def list_leads(request):

    if request.user.is_superuser:
        leads = Lead.objects.all()
    else :
        try:
            agent = request.user.agent
            leads = Lead.objects.filter(agent=agent)
        except : 
            return redirect('not_authorized')
    context = {
        'leads':leads,
    }
    return render(request,'leads/leads_list.html',context)


############## Loss Lead View #####################
@login_required
def loss_lead(request, pk):
    # Get the Lead instance
    lead = Lead.objects.get(id=pk)

    # Create a LossLead instance and copy data from the Lead instance
    LossLead.objects.create(
        first_name=lead.first_name,
        last_name=lead.last_name,
        phone_number=lead.phone_number,
        email=lead.email,
        age=lead.age,
        source=lead.source,
        agent=lead.agent,
        lead=lead  # Optional reference to the original Lead
    )

    # Delete the Lead instance
    lead.delete()

    return redirect('list_loss_leads')


########## List of loss Leads view##############
@login_required
def list_loos_leads(request):
    if request.user.is_superuser :
        loss_leads = LossLead.objects.all()
        pass
    else : 
        agent = request.user.agent
        loss_leads = LossLead.objects.filter(agent=agent)
    
    print("prospet perdus ====================>", loss_leads)
    context = {
        'loss_leads':loss_leads,
    }
    return render(request,'leads/loss_leads_list.html',context)



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
    # Get the Lead instance
    lead = Lead.objects.get(id=pk)

    # Create a LossLead instance and copy data from the Lead instance
    Client.objects.create(
        first_name=lead.first_name,
        last_name=lead.last_name,
        phone_number=lead.phone_number,
        email=lead.email,
        age=lead.age,
        source=lead.source,
        agent=lead.agent,
        lead=lead  # Optional reference to the original Lead
    )

    # Delete the Lead instance
    lead.delete()

    return redirect('list_client')

########## List Client ###########

def list_client(request):
    if request.user.is_superuser:
        clients = Client.objects.all()
    else : 
        agent = request.user.agent 
        clients = Client.objects.filter(agent=agent)

    context = {
        'clients':clients
    }

    return render(request,'clients/list_clients.html',context)