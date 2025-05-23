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
    friends = models.ManyToManyField('self', symmetrical=False, related_name='friends_of')

    def clothing_owned(self):
        """
        Get all the clothing this user owns, sort them into hats, shirts, 
        and shoes, then return a tuple of lists.
        """
        hats = []
        shirts = []
        shoes = []
        backgrounds = []

        for item in self.owns.all():
            if item.clothing_type == "Hat":
                hats.append(item)
            elif item.clothing_type == "Shirt":
                shirts.append(item)
            elif item.clothing_type == "Shoes":
                shoes.append(item)
            elif item.clothing_type == "Background":
                backgrounds.append(item)

        return hats, shirts, shoes, backgrounds


    def buy_clothing(self, clothing):
        """
        Purchase new clothing for pet. Returns True if purchase is valid.
        """
        can_buy = self.is_purchasable(clothing)
        if can_buy:
            self.coins = self.coins - clothing.price
            self.owns.add(clothing)
        return can_buy


    def is_purchasable(self, clothing):
        """
        Returns True if purchase is valid.
        """
        if not self.owns.filter(clothing_id=clothing.clothing_id).exists(): #checks to see if clothing is not in owned
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
        ("Background", "Background"),
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
    background = models.ForeignKey(Clothing, on_delete=models.SET_NULL, null=True, related_name='pets_with_this_background', default = None)
    image_path = models.CharField(max_length=255, blank=False, null=False, default='images/')
    level = models.IntegerField(default=1)
        
    def is_wearing(self):
        """
        Returns tuple (hat, shirt, shoes) that the pet is wearing
        """
        return (self.hat, self.shirt, self.shoes, self.background)
        
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
   
    def neededXP(self):
        """
        Amount of XP needed before level up
        """
        return ((self.level * 100) - self.xp)
    
    def addXP (self, gainedXP):
        """
        Adds XP and Levels Up Pet if threshold is met
        """
        while (gainedXP > 0):
            XP = self.neededXP()
            gainedXP -= XP
            if (gainedXP >= 0):
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

    def calculateXP(self, reps):
        """
        If the reps are higher than max_reps then cap XP gain
        """
        if (reps > self.max_reps):
            return round(self.tier * self.max_reps * 0.5)
        else: 
            return round(self.tier * reps * 0.5)
            
    def calculateCoins(self, reps): 
        """
        If the reps are higher than max_reps then cap Coin gain
        """
        if (reps > self.max_reps):
            return round(self.tier * self.max_reps * 0.1)
        else: 
            return round(self.tier * reps * 0.1)

class FriendRequest(models.Model):
    from_user = models.ForeignKey(FPUser, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(FPUser, related_name='received_requests', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"{self.from_user.username} → {self.to_user.username}"