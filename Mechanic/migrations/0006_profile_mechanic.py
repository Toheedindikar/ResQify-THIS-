# Generated by Django 4.2.7 on 2024-02-02 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mechanic', '0005_booking_status_booking_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile_mechanic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=1000, null=True)),
                ('no_of_bookings', models.CharField(blank=True, max_length=5000, null=True)),
                ('rating', models.CharField(blank=True, max_length=200, null=True)),
                ('mech_name', models.CharField(blank=True, max_length=500, null=True)),
                ('mech_username', models.CharField(blank=True, max_length=500, null=True)),
            ],
            options={
                'db_table': 'Profile_mechanic',
            },
        ),
    ]
