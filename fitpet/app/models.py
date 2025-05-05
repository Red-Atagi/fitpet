from django.db import models
from django.contrib.auth.models import User


class FPUser(models.Model):
    '''
    All FitPet users. Uses the Django User class to handle authentication.
    '''
    user_id = models.AutoField(primary_key=True)
    djuser = models.ForeignKey(User, on_delete=models.CASCADE)  # handles authentication
    coins = models.IntegerField(default=0)
    username = models.CharField(max_length=255, default=None)
    name = models.CharField(max_length=255, default=None)
    owns = models.ManyToManyField('Clothing', related_name='users')

    def clothing_owned(self):
        """
        Get all the clothing this user owns, sort them into hats, shirts, 
        and shoes, then return a tuple of lists.
        """
        hats = []
        shirts = []
        shoes = []

        for item in self.owns.all():
            if item.clothing_type == "Hat":
                hats.append(item)
            elif item.clothing_type == "Shirt":
                shirts.append(item)
            elif item.clothing_type == "Shoes":
                shoes.append(item)

        return hats, shirts, shoes


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

    def addCoins(self, gainedCoins):
        """
        Adds coins to the users wallet
        """
        self.coins += gainedCoins
        return

class Clothing(models.Model):
    CLOTHING_CHOICES = [
        ("Hat", "Hat"),
        ("Shirt", "Shirt"),
        ("Shoes", "Shoes"),
    ]
    
    clothing_id = models.AutoField(primary_key=True)
    price = models.IntegerField()
    clothing_type = models.CharField(choices=CLOTHING_CHOICES, max_length=255)
    image_path = models.CharField(max_length=255, blank=False, null=False, default='images/')

class Pet(models.Model):
    pet_id = models.AutoField(primary_key=True)
    xp = models.IntegerField(default=0)
    name = models.CharField(max_length=255, default=None)
    owner = models.ForeignKey(FPUser, on_delete=models.CASCADE)
    hat = models.ForeignKey(Clothing, on_delete=models.SET_NULL, null=True, related_name='pets_with_this_hat', default=None)
    shirt = models.ForeignKey(Clothing, on_delete=models.SET_NULL, null=True, related_name='pets_with_this_shirt', default = None)
    shoes = models.ForeignKey(Clothing, on_delete=models.SET_NULL, null=True, related_name='pets_with_these_shoes', default = None)
    image_path = models.CharField(max_length=255, blank=False, null=False, default='images/')
    level = models.IntegerField(default=1)
        
    def is_wearing(self):
        """
        Returns tuple (hat, shirt, shoes) that the pet is wearing
        """
        return (self.hat, self.shirt, self.shoes)
        
    def getLevel(self):
        """
        Returns the pet level
        """
        return (self.level)
    
    def getXP(self):
        """
        Returns the Pet's XP
        """
        return (self.xp)
    
    
    def addXP (self, gainedXP):
        """
        Adds XP and Levels Up Pet if threshold is met
        """
        while (gainedXP > 0):
            neededXP = (self.level * 100) - self.xp
            gainedXP -= neededXP
            if (gainedXP > 0):
                self.level += 1
                self.xp = 0
            else: 
                self.xp = (self.level * 100) + gainedXP
        return
        
        
    
class Exercise(models.Model):
    exercise_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, default=None)
    tier = models.IntegerField() # degree of difficulty
    max_reps = models.IntegerField()

    def calculateXP(max_reps, tier, reps):
        """
        If the reps are higher than max_reps then cap XP gain
        """
        if (reps > max_reps):
            return round(tier * max_reps * 0.5)
        else: 
            return round(tier * reps * 0.5)
            
    def calculateCoins(max_reps, tier, reps): 
        """
        If the reps are higher than max_reps then cap Coin gain
        """
        if (reps > max_reps):
            return round(tier * max_reps * 0.1)
        else: 
            return round(tier * reps * 0.1)
        
    def canLevelUP(self, gainedXP):
        """
        Returns true if there is a level up
        """
        neededXP = (Pet.getLevel * 100) - Pet.getXP
        return (neededXP <= gainedXP)
    
    
    