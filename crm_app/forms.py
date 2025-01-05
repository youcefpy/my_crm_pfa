from django.forms import ModelForm
from .models import Lead,Agent,User


class LeadForm(ModelForm):
    class Meta:
        model = Lead
        fields = '__all__'

class AgentForm(ModelForm):
    class Meta : 
        model = User
        fields = '__all__'

    