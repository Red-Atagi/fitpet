from django.db import models
from django.contrib.auth.models import User

class FPUser(models.Model):
    '''
    All FitPet users. Uses the Django User class to handle authentication.
    '''
    
    user_id = models.AutoField(primary_key=True)
    djuser = models.ForeignKey(User, on_delete=models.CASCADE) # handles authentication
    coins = models.IntegerField(default=0)
    username = models.CharField(max_length=255, default=None)
    name = models.CharField(max_length=255, default=None)
    owns = models.ManyToManyField('Clothing', related_name='users')

class Pet(models.Model):
    pet_id = models.AutoField(primary_key=True)
    xp = models.IntegerField(default=0)
    name = models.CharField(max_length=255, default=None)
    owner = models.ForeignKey(FPUser, on_delete=models.CASCADE)
    wearing = models.ManyToManyField('Clothing', related_name='pets')
    
class Exercise(models.Model):
    exercise_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, default=None)
    level = models.IntegerField()
    max_reps = models.IntegerField()
    
class Clothing(models.Model):
    CLOTHING_CHOICES = [
        ("Hat", "Hat"),
        ("Shirt", "Shirt"),
        ("Shoes", "Shoes"),
    ]
    
    clothing_id = models.AutoField(primary_key=True)
    price = models.IntegerField()
    clothing_type = models.CharField(choices=CLOTHING_CHOICES, max_length=255)
    image_path = models.CharField(max_length=255)
    