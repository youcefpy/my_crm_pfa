# dashboard_app/services.py
from crm_app.models import Lead,Agent
from django.db.models.functions import TruncMonth,TruncDay
from django.db.models import Count
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
    from django.db import models
    agents_data = (
        Agent.objects.annotate(
            total_clients=Count('lead__client', distinct=True),
            total_prospects_lost=Count('lead', filter=~models.Q(lead__is_client=True))
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

def get_lost_prospects_by_source():

    lost_prospects_by_source = (
        Lead.objects.filter(is_client=False)
        .values('source')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    labels = [entry['source'] for entry in lost_prospects_by_source]
    data = [entry['total'] for entry in lost_prospects_by_source]

    return {
        'labels': json.dumps(labels),
        'data': json.dumps(data),
    }


def get_top_performing_agents():
    agents_data = (
        Agent.objects.annotate(
            total_clients=Count('lead__client', distinct=True),
            conversion_rate=(Count('lead__client', distinct=True) * 100) / Count('lead')
        )
        .order_by('-total_clients')
    )

    labels = [agent.user.username for agent in agents_data]
    data = [agent.total_clients for agent in agents_data]
    conversion_rate = [agent.conversion_rate for agent in agents_data]

    return {
        'labels': json.dumps(labels),
        'data': json.dumps(data),
        'conversion_rate': json.dumps(conversion_rate),
    }
