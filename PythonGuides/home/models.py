from django.db import models

class EmpLogin(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    password = models.CharField(max_length=8)
    class Meta:
        db_table="EmpLogin"

class UsersCustomer(models.Model):
    name = models.CharField(max_length=500)
    username = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)
    email = models.EmailField(max_length = 254)
    password = models.CharField(max_length=50)
    class Meta:
        db_table="UsersCustomer"


class BookMechanic(models.Model):
    issueid = models.CharField(max_length=1000,blank=True, null=True)
    address = models.CharField(max_length=500,blank=True, null=True)
    zipcode = models.CharField(max_length=100,blank=True, null=True)
    vehicleType = models.CharField(max_length=100,blank=True, null=True)
    vehicleNo = models.CharField(max_length=100,blank=True, null=True)
    issuedesc = models.CharField(max_length=500,blank=True, null=True)
    phone = models.CharField(max_length=500,blank=True, null=True)
    lat = models.CharField(max_length=200,blank=True, null=True)
    lng = models.CharField(max_length=200,blank=True, null=True)
    class Meta:
        db_table="BookMechanic"

class UsersCurrentAddress(models.Model):
    issueid = models.CharField(max_length=1000,blank=True, null=True)
    address = models.CharField(max_length=500,blank=True, null=True)
    zipcode = models.CharField(max_length=100,blank=True, null=True)
    vehicleType = models.CharField(max_length=100,blank=True, null=True)
    vehicleNo = models.CharField(max_length=100,blank=True, null=True)
    issuedesc = models.CharField(max_length=500,blank=True, null=True)
    phone = models.CharField(max_length=500,blank=True, null=True)
    lat = models.CharField(max_length=200,blank=True, null=True)
    lng = models.CharField(max_length=200,blank=True, null=True)
    username = models.CharField(max_length=100)
    
    class Meta:
        db_table="UsersCurrentAddress"


