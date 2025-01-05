from django.contrib import admin
from .models import Agent,Lead,User


# Register your models here.

class AgentAdmin(admin.ModelAdmin):
    #get all the fields of the model Agent
    list_display=[field.name for field in Agent._meta.fields]

class LeadAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Lead._meta.fields]

class UserAdmin(admin.ModelAdmin):
    list_display = [field.name for field in User._meta.fields]

admin.site.register(Agent,AgentAdmin)
admin.site.register(Lead,LeadAdmin)
admin.site.register(User,UserAdmin)