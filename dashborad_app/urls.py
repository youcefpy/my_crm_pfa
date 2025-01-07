from django.urls import path
from .views import index_dashborad
urlpatterns = [
    path('',index_dashborad,name="dashborad")
]