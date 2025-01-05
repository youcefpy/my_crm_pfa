from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import index,details,creat_lead,create_agent,list_agents,update_lead,delete_lead,send_email_to_lead

urlpatterns = [
    path('',index,name='index'),
    path('details/<pk>',details,name="details_page"),
    path('cree-prospet/',creat_lead,name="create_lead"),
    path('mis-a-jour-prospet/<pk>',update_lead,name="update_lead"),
    path('supprimer-prospet/<pk>',delete_lead,name='delete_lead'),
    path('cree-agent/',create_agent,name="create_agent"),
    path('list-agents',list_agents,name='list_agents'),
    path('send-email/<pk>',send_email_to_lead,name="send_email"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
