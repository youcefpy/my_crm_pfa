import json
from django.shortcuts import render
from .services import (
    get_dashboard_data,
    get_prospects_by_source,
    get_agents_comparison,
    get_prospet_by_month,
    get_lost_prospects_by_source,
    get_top_performing_agents
)

def dashboard_index(request):
    context = {
        'get_dashboard_data':get_dashboard_data(),
        'prospects_by_source': get_prospects_by_source(),
        'agents_comparison': get_agents_comparison(),
        'leads_by_month': get_prospet_by_month(),
        'lost_prospects_by_source': get_lost_prospects_by_source(),
        'top_performing_agents': get_top_performing_agents(),
        }
    
    return render(request, 'dashboard/index.html', context)
