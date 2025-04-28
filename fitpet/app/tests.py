from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from app.models import *

class CreateAcountTestCase(TestCase):
    def setUp(self):
        ...
    
    def test_1(self):
        ...

class ShopTestCase(TestCase):
    def setUp(self):

        shop = Shop (hat, shirt, shoes)
        self.pet1 = Pet.objects.create(owner=self.fpuser1, name='PetOne', image_path="images/test_pet.png")
        ...
    
    def test_get_hat(self):
        ...

    def test_get_shirt(self):
        ...

    def test_get_shoes(self):
        ...
    
    def test_display_clothing_bad_id(self):
        ...

    def test_display_clothing_good_id(self):
        ...
    
    def test_get_clothes_not_owned_owns_nothing(self):
        ...

    def test_get_clothes_not_owned_owns_some(self):
        ...

    def test_get_clothes_not_owned_owns_all(self):
        ...
    
    def test_buy_clothes_not_enough_money(self):
        ...

    def test_buy_clothes_enough_money(self):
        ...
    


class DressPetTestCase(TestCase):
    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(username='user1', password='testpass')
        self.user2 = User.objects.create_user(username='user2', password='testpass')
        self.user3 = User.objects.create_user(username='user3', password='testpass')

        # Create FPUser instances
        self.fpuser1 = FPUser.objects.create(djuser=self.user1, username='user1', name='User One')
        self.fpuser2 = FPUser.objects.create(djuser=self.user2, username='user2', name='User Two')
        self.fpuser3 = FPUser.objects.create(djuser=self.user3, username='user3', name='User Three')
        
        # Get clothing items
        clothing1 = Clothing.objects.get(clothing_id = 1) # hat1
        clothing2 = Clothing.objects.get(clothing_id = 2) # hat2
        clothing3 = Clothing.objects.get(clothing_id = 3) # shirt1
        clothing4 = Clothing.objects.get(clothing_id = 4) # shirt2
        clothing5 = Clothing.objects.get(clothing_id = 5) # shoes1
        clothing6 = Clothing.objects.get(clothing_id = 6) # shoes2
        
        # Assign clothing to users
        self.fpuser1.owns.add(clothing1, clothing2, clothing3, clothing4, clothing5, clothing6)
        self.fpuser2.owns.add(clothing1, clothing3, clothing5)
        
        # Create Pet instances
        self.pet1 = Pet.objects.create(owner=self.fpuser1, name='PetOne', image_path="images/test_pet.png")
        self.pet2 = Pet.objects.create(owner=self.fpuser2, name='PetTwo', image_path="images/test_pet.png")
        self.pet3 = Pet.objects.create(owner=self.fpuser3, name='PetThree', image_path="images/test_pet.png")
    
    def test_1(self):
        # Log in
        self.client.login(username='user1', password='testpass')

        # Get dress page
        response = self.client.get(reverse('display_dress_page'))
        self.assertEqual(response.status_code, 200)

        # Check all clothing options are displayed
        content = response.content.decode()
        self.assertIn("test_hat1.png", content)
        self.assertIn("test_hat2.png", content)
        self.assertIn("test_shirt1.png", content)
        self.assertIn("test_shirt2.png", content)
        self.assertIn("test_shoes1.png", content)
        self.assertIn("test_shoes2.png", content)

        # Changing clothes
        response = self.client.post(reverse('update_clothing'), {
            'clothing_id': 2 
        })
        self.assertEqual(response.status_code, 200)

        # Refresh pet data
        self.pet1.refresh_from_db()
        self.assertEqual(self.pet1.hat.clothing_id, 2)

        # Change again
        response = self.client.post(reverse('update_clothing'), {
            'clothing_id': 1  # Switching back to hat1
        })
        self.assertEqual(response.status_code, 200)
        self.pet1.refresh_from_db()
        self.assertEqual(self.pet1.hat.clothing_id, 1)
    
    def test_2(self):
        # Log in
        self.client.login(username='user2', password='testpass')

        # Get dress page
        response = self.client.get(reverse('display_dress_page'))
        self.assertEqual(response.status_code, 200)

        # Check correct clothing options are displayed
        content = response.content.decode()
        self.assertIn("test_hat1.png", content)
        self.assertNotIn("test_hat2.png", content)
        self.assertIn("test_shirt1.png", content)
        self.assertNotIn("test_shirt2.png", content)
        self.assertIn("test_shoes1.png", content)
        self.assertNotIn("test_shoes2.png", content)

        # Simulate clothing changes
        response = self.client.post(reverse('update_clothing'), {
            'clothing_id': 1
        })
        self.assertEqual(response.status_code, 200)

        self.pet2.refresh_from_db()
        self.assertEqual(self.pet2.hat.clothing_id, 1)

        response = self.client.post(reverse('update_clothing'), {
            'clothing_id': 3
        })
        self.assertEqual(response.status_code, 200)

        self.pet2.refresh_from_db()
        self.assertEqual(self.pet2.shirt.clothing_id, 3)

    def test_3(self):
        # Log in
        self.client.login(username='user3', password='testpass')

        # Get dress page
        response = self.client.get(reverse('display_dress_page'))
        self.assertEqual(response.status_code, 200)

        # Check nothing is displayed
        content = response.content.decode()
        self.assertNotIn("test_hat1.png", content)
        self.assertNotIn("test_hat2.png", content)
        self.assertNotIn("test_shirt1.png", content)
        self.assertNotIn("test_shirt2.png", content)
        self.assertNotIn("test_shoes1.png", content)
        self.assertNotIn("test_shoes2.png", content)

class WorkoutTestCase(TestCase):
    def setUp(self):
        ...
    
    def test_1(self):
        ...