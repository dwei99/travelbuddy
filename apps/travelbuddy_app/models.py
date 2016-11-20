from __future__ import unicode_literals

from django.db import models

# Create your models here.
class UserManager(models.Manager):
    def login(self, email, password):
        #search for user record if there is a match return user, if not return none
        user = User.objects.filter(email = email).filter(password = password)
        print user
        if not user:
            print "fail"
            return False
        else:
            print "true"
            return True

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=100)
    create_dt = models.DateTimeField(auto_now_add=True)
    update_dt = models.DateField(auto_now_add=True)
    objects = UserManager()

class Trip(models.Model):
    destination = models.CharField(max_length= 255)
    description = models.TextField(max_length=1000, default= None)
    trip_start_dt = models.DateField(auto_now_add=False)
    trip_end_dt = models.DateField(auto_now_add=False)
    user = models.ForeignKey(User)
    create_dt = models.DateField(auto_now_add=True)
    update_dt = models.DateField(auto_now=True)

class TravelPlan(models.Model):
    create_dt = models.DateField(auto_now_add=True)
    update_dt = models.DateField(auto_now_add=True)
    trip = models.ForeignKey(Trip)
    user = models.ForeignKey(User)
