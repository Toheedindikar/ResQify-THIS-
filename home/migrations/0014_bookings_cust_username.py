# Generated by Django 4.2.7 on 2024-01-28 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_bookings'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookings',
            name='cust_username',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
