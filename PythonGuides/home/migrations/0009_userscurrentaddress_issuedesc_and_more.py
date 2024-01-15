# Generated by Django 4.2.7 on 2024-01-15 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_alter_bookmechanic_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userscurrentaddress',
            name='issuedesc',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='userscurrentaddress',
            name='issueid',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='userscurrentaddress',
            name='phone',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='userscurrentaddress',
            name='vehicleNo',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='userscurrentaddress',
            name='vehicleType',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='userscurrentaddress',
            name='zipcode',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
