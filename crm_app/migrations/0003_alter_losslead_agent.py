# Generated by Django 5.1.4 on 2025-01-10 20:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0002_alter_client_agent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='losslead',
            name='agent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm_app.agent'),
        ),
    ]
