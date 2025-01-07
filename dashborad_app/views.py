from django.shortcuts import render

# Create your views here.


def index_dashborad(request):
    
    return render(request,'index.html')