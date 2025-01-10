from django.contrib import admin
from .models import Agent,Lead,User,Client,LossLead


# Register your models here.

class AgentAdmin(admin.ModelAdmin):
    #get all the fields of the model Agent
    list_display=[field.name for field in Agent._meta.fields]

class LeadAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Lead._meta.fields]

class UserAdmin(admin.ModelAdmin):
    list_display = [field.name for field in User._meta.fields]

class ClientAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Client._meta.fields]


class LossLeadAdmin(admin.ModelAdmin):
    list_display=[field.name for field in LossLead._meta.fields]

admin.site.register(Agent,AgentAdmin)
admin.site.register(Lead,LeadAdmin)
admin.site.register(User,UserAdmin)
admin.site.register(Client,ClientAdmin)
admin.site.register(LossLead,LossLeadAdmin)