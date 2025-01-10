from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import path
from .views import (
    index,details,create_lead,list_agents,update_lead,loss_lead,send_email_to_lead,
    SignupView,logout_view,create_agent,create_client,list_client,not_authorized,list_loos_leads,list_leads
    )

urlpatterns = [
    path('',index,name='index'),
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',logout_view,name='logout'),
    path('signup/',SignupView.as_view(),name="signup"),
    path('details/<pk>',details,name="details_page"),
    path('cree-prospet/',create_lead,name="create_lead"),
    path('liste-prospet/',list_leads,name="list_leads"),
    path('mis-a-jour-prospet/<pk>',update_lead,name="update_lead"),
    path('prospet-perdu/<pk>',loss_lead,name='loss_lead'),
    path('list-prospet-perdu',list_loos_leads,name="list_loss_leads"),
    path('cree-agent/', create_agent, name='create_agent'),
    path('list-agents',list_agents,name='list_agents'),
    path('send-email/<pk>',send_email_to_lead,name="send_email"),
    path('cree-client/<pk>',create_client,name='create_client'),
    path('liste-client/',list_client,name='list_client'),
    path('not-authorized/', not_authorized, name='not_authorized'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
