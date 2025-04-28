from django.db import models
from django.contrib.auth.models import User


class FPUser(models.Model):
    '''
    All FitPet users. Uses the Django User class to handle authentication.
    '''
    def __init__(self):
        self.user_id = models.AutoField(primary_key=True)
        self.djuser = models.ForeignKey(User, on_delete=models.CASCADE) # handles authentication
        self.coins = models.IntegerField(default=0)
        self.username = models.CharField(max_length=255, default=None)
        self.name = models.CharField(max_length=255, default=None)
        self.owns = models.ManyToManyField('Clothing', related_name='users')


    def clothing_owned(self):
        """
        Get all the clothing this user owns, sort them into hats, shirts, 
        and shoes, then return a tuple of lists.
        """
        all_clothes = {}
        for item in self.owns:
            if item.clothing_type == "Hat":
                if all_clothes.get("Hats"):
                    all_clothes["Hats"].append()
                else:
                    all_clothes["Hats"] = [item]
            if item.clothing_type == "Shirt":
                if all_clothes.get("Shirts"):
                    all_clothes["Shirts"].append()
                else:
                    all_clothes["Shirts"] = [item]
            if item.clothing_type == "Shoes":
                if all_clothes.get("Shoes"):
                    all_clothes["Shoes"].append()
                else:
                    all_clothes["Shoes"] = [item]
        return all_clothes


    def buy_clothing(self, clothing):
        """
        Purchase new clothing for pet. Returns True if purchase is valid.
        """
        can_buy = self.is_purchasable(clothing)
        if not can_buy:
            print("Not enough coins!")
        else:
            self.coins = self.coins - clothing.price
            self.owns.add(clothing)
            print(f"You purchased {clothing.clothing_id} ({clothing.clothing_type}) for {clothing.price}🤑🥳!")
        return can_buy


    def is_purchasable(self, clothing):
        """
        Returns True if purchase is valid.
        """
        if self.coins >= clothing.price:
            return True
        return False


class Pet(models.Model):
    def __init__(self):
        self.pet_id = models.AutoField(primary_key=True)
        self.xp = models.IntegerField(default=0)
        self.name = models.CharField(max_length=255, default=None)
        self.owner = models.ForeignKey(FPUser, on_delete=models.CASCADE)
        self.hat = models.ForeignKey('Clothing', default=None)
        self.shirt = models.ForeignKey('Clothing', default=None)
        self.shoes = models.ForeignKey('Clothing', default=None)
        self.image_path = models.CharField(max_length=255)
        
    def is_wearing(self):
        """
        Returns tuple (hat, shirt, shoes) that the pet is wearing
        """
        return (self.hat, self.shirt, self.shoes)
        
    
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
    