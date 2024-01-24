# Generated by Django 4.2.7 on 2024-01-08 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_bookmechanic_lat_bookmechanic_lng'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsersCurrentAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.CharField(blank=True, max_length=200, null=True)),
                ('lng', models.CharField(blank=True, max_length=200, null=True)),
                ('username', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'UsersCurrentAddress',
            },
        ),
    ]