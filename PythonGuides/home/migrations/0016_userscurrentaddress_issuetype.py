# Generated by Django 4.2.7 on 2024-02-01 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_profile_mech_name_profile_mech_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='userscurrentaddress',
            name='issuetype',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
