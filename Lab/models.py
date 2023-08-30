from django.db import models
from django.contrib.auth.models import User


class Lab(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=500) 
    pincode = models.IntegerField()
    state = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Patient(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=30)
    test_name = models.CharField(max_length=100)
    aadhar_no = models.IntegerField()
    contact = models.IntegerField()
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tests = models.ManyToManyField("Test")


class Bill(models.Model):
    total = models.IntegerField(default=0,blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)


class Test(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.IntegerField(null=True,blank=True)
    quantity = models.IntegerField(null=True,blank=True)
    status = models.BooleanField(default=False)
    sub_total= models.DecimalField(max_digits=10,decimal_places=2,default=0.0)
    value = models.CharField(max_length=100,null=True,blank=True)







   


