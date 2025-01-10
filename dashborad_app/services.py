# dashboard_app/services.py
from crm_app.models import Lead,Agent,LossLead,Client
from django.db.models.functions import TruncMonth,TruncDay
from django.db.models import Count, F
import json


def get_dashboard_data():
    leads_by_day = (
        Lead.objects.annotate(day=TruncDay('created_at'))
        .values('day')
        .annotate(total=Count('id'))
        .order_by('day')
    )

    labels = [entry['day'].strftime('%d-%m-%Y') for entry in leads_by_day]
    data = [entry['total'] for entry in leads_by_day]

    return {
        'labels': json.dumps(labels),
        'data': json.dumps(data),
    }

def get_prospects_by_source():
    prospects_by_source = (
        Lead.objects.values('source')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    labels = [entry['source'] for entry in prospects_by_source]
    data = [entry['total'] for entry in prospects_by_source]

    return {
        'labels': json.dumps(labels),
        'data': json.dumps(data),
    }


def get_agents_comparison():
    
    agents_data = (
        Agent.objects.annotate(
            total_clients=Count('client', distinct=True),
            total_prospects_lost=Count('id')
        )
    )

    labels = [agent.user.username for agent in agents_data]
    clients_data = [agent.total_clients for agent in agents_data]
    prospects_lost_data = [agent.total_prospects_lost for agent in agents_data]

    return {
        'labels': json.dumps(labels),
        'clients_data': json.dumps(clients_data),
        'prospects_lost_data': json.dumps(prospects_lost_data),
    }


def get_prospet_by_month():
    leads_by_month = (
        Lead.objects.all().annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(total=Count('id'))
        .order_by('month')
    )
    labels = [entry['month'].strftime('%Y-%m') for entry in leads_by_month]
    data = [entry['total'] for entry in leads_by_month]

    return {
        'labels': json.dumps(labels),
        'data': json.dumps(data),
    }

def get_lost_prospects_by_agent(): 
    
    lost_prospects_by_agent = (
        LossLead.objects.values(agent_username=F('agent__user__username'))  
        .annotate(total=Count('id'))  
        .order_by('-total')  
    )

    
    labels = [entry['agent_username'] for entry in lost_prospects_by_agent]  
    data = [entry['total'] for entry in lost_prospects_by_agent] 
    return {
        'labels': json.dumps(labels),
        'data': json.dumps(data),
    }


def get_lost_lead_by_source():
    lost_lead_by_source = (
        LossLead.objects.values('source')
        .annotate(total=Count('id'))
        .order_by('-total')
    )
    labels = [entry['source'] for entry in lost_lead_by_source]
    data = [entry['total'] for entry in lost_lead_by_source]

    return {
        'labels':json.dumps(labels),
        'data':json.dumps(data)
    }

def get_total_leads():
    # Group and count Leads by day
    leads_by_day = (
        Lead.objects.annotate(day=TruncDay('created_at'))
        .values('day')
        .annotate(total_leads=Count('id'))
    )
    win_lead_day = (
        Client.objects.annotate(day=TruncDay('created_at'))
        .values('day')
        .annotate(total_clients=Count('id'))
    )

    # Group and count LossLeads by day
    loss_leads_by_day = (
        LossLead.objects.annotate(day=TruncDay('created_at'))
        .values('day')
        .annotate(total_loss_leads=Count('id'))
    )

    # Combine the two querysets into a dictionary
    combined_counts = {}

    for lead in leads_by_day:
        day = lead['day']
        combined_counts[day] = combined_counts.get(day, 0) + lead['total_leads']

    for client in win_lead_day:
        day = client['day']
        combined_counts[day] = combined_counts.get(day, 0) + client['total_clients']

    for loss_lead in loss_leads_by_day:
        day = loss_lead['day']
        combined_counts[day] = combined_counts.get(day, 0) + loss_lead['total_loss_leads']

    # Sort the combined results by day
    sorted_days = sorted(combined_counts.keys())
    labels = [day.strftime('%d-%m-%Y') for day in sorted_days]
    data = [combined_counts[day] for day in sorted_days]

    return {
        'labels': json.dumps(labels),
        'data': json.dumps(data),
    }