from django.forms import ModelForm
from .models import Lead,Agent,User
from django.contrib.auth.forms import UserCreationForm



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User  
        fields = ['username', 'first_name','last_name','email', 'password1', 'password2','date_joined']  


class LeadForm(ModelForm):
    def __init__(self, *args, **kwargs):
        exclude_agent = kwargs.pop('exclude_agent', False)  
        super().__init__(*args, **kwargs) 
        if exclude_agent:
            self.fields.pop('agent')

    class Meta:
        model = Lead
        fields = '__all__'


class AgentForm(ModelForm):
    class Meta:
        model = Agent
        fields='__all__'