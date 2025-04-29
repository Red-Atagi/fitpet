from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from app.models import *
from .models import FPUser, Pet, Clothing


class CreateAcountTestCase(TestCase):
    def testValidUser(self):
        response = self.client.post(reverse('register'), {
            'username': 'testingUsername',
            'password1': 'testPass189',
            'password2': 'testPass189'
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testingUsername').exists())

    def testUserExists(self):
        User.objects.create_user(username='existingUser', password='testpass')

        response = self.client.post(reverse('register'), {
            'username': 'existingUser',
            'password1': 'testPass123',
            'password2': 'testPass123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A user with that username already exists", status_code=200)
    
    def test_passwords_do_not_match(self):
        response = self.client.post(reverse('register'), {
            'username': 'newUser',
            'password1': 'testPass123',
            'password2': 'differentPass123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The two password fields didn’t match", status_code=200)
    
    def test_weak_password(self):
        response = self.client.post(reverse('register'), {
            'username': 'weakpassuser',
            'password1': '123',
            'password2': '123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This password is too short", status_code=200)
    
    def test_empty_form_submission(self):
        response = self.client.post(reverse('register'), {})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required", status_code=200)
    
    def test_username_too_long(self):
        long_username = 'a' * 200
        response = self.client.post(reverse('register'), {
            'username': long_username,
            'password1': 'ValidPass123',
            'password2': 'ValidPass123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ensure this value has at most", status_code=200)


class UserAuthTestCase(TestCase):
    """Tests for login, logout, password change, password reset."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='oldpassword')

    def test_login_success(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'oldpassword'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_login_failure(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_logout(self):
        self.client.login(username='testuser', password='oldpassword')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302) 
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_password_change_success(self):
        self.client.login(username='testuser', password='oldpassword')
        response = self.client.post(reverse('password_change'), {
            'old_password': 'oldpassword',
            'new_password1': 'newsecurepass123',
            'new_password2': 'newsecurepass123'
        })
        self.assertEqual(response.status_code, 302)

        # Logout and try logging in with the new password
        self.client.logout()
        login_success = self.client.login(username='testuser', password='newsecurepass123')
        self.assertTrue(login_success)

    def test_password_reset_request(self):
        response = self.client.post(reverse('password_reset'), {
            'email': self.user.email if self.user.email else 'test@example.com'
        })
        self.assertEqual(response.status_code, 302)

    def test_cannot_access_secure_page_after_logout(self):
        self.client.login(username='testuser', password='oldpassword')

        self.client.logout()

        response = self.client.get(reverse('secure_page_url'))
        self.assertEqual(response.status_code, 302)






class ShopTestCase(TestCase):
    def setUp(self):
        self.userNoClothes = User.objects.create_user(
            username="userNoClothes", password="testpass"
        )
        self.userSomeClothes = User.objects.create_user(
            username="userSomeClothes", password="testpass"
        )
        self.userAllClothes = User.objects.create_user(
            username="userAllClothes", password="testpass"
        )

        self.fpuserNoClothes = FPUser.objects.create(
            djuser=self.userNoClothes, username="userNoClothes", name="User NoClothes", coins=50
        )
        self.fpuserSomeClothes = FPUser.objects.create(
            djuser=self.userSomeClothes, username="userSomeClothes", name="User SomeClothes", coins=50
        )
        self.fpuserAllClothes = FPUser.objects.create(
            djuser=self.userAllClothes, username="userAllClothes", name="User AllClothes", coins=50
        )

        # Create test clothing items
        self.hat1 = Clothing.objects.create(price=10, clothing_type="Hat", image_path="images/hat1.png")
        self.hat2 = Clothing.objects.create(price=10, clothing_type="Hat", image_path="images/hat2.png")
        self.shirt1 = Clothing.objects.create(price=50, clothing_type="Shirt", image_path="images/shirt1.png")
        self.shirt2 = Clothing.objects.create(price=50, clothing_type="Shirt", image_path="images/shirt2.png")
        self.shoes1 = Clothing.objects.create(price=100, clothing_type="Shoes", image_path="images/shoes1.png")
        self.shoes2 = Clothing.objects.create(price=100, clothing_type="Shoes", image_path="images/shoes2.png")

        #add only somes items to some clothes user
        self.fpuserSomeClothes.owns.add(self.hat1, self.shirt1)
    
        #add all the clothes to own to user
        all_clothing = Clothing.objects.all()
        for item in all_clothing:
            self.fpuserAllClothes.owns.add(item)

        self.petNone = Pet.objects.create(
            owner=self.fpuserNoClothes, 
            name="PetNone", 
            image_path="images/test_pet.png"
        )

        self.petSome = Pet.objects.create(
            owner=self.fpuserSomeClothes,
            name="PetSome",
            image_path="images/test_pet.png",
        )

        self.petAll = Pet.objects.create(
            owner=self.fpuserAllClothes, 
            name="PetAll", 
            image_path="images/test_pet.png"
        )

    def test_shop_no_clothing_owned(self):
        # Log in
        self.client.login(username="userNoClothes", password="testpass")

        # Get dress page
        response = self.client.get(reverse("shop_page"))
        self.assertEqual(response.status_code, 200)

        #seperate the ids into a list of all unowned items
        hat_ids = [hat.clothing_id for hat in response.context['hats_unowned']]
        shirt_ids = [shirt.clothing_id for shirt in response.context['shirts_unowned']]
        shoe_ids = [shoe.clothing_id for shoe in response.context['shoes_unowned']]

        #all hats and clothes should be returned from page
        self.assertIn(self.hat1.clothing_id, hat_ids)
        self.assertIn(self.hat2.clothing_id, hat_ids)
        self.assertIn(self.shirt1.clothing_id, shirt_ids)
        self.assertIn(self.shirt2.clothing_id, shirt_ids)
        self.assertIn(self.shoes1.clothing_id, shoe_ids)
        self.assertIn(self.shoes2.clothing_id, shoe_ids)

    def test_shop_some_clothing_owned(self):
        # Log in
        self.client.login(username="userSomeClothes", password="testpass")

        # Get dress page
        response = self.client.get(reverse("shop_page"))
        self.assertEqual(response.status_code, 200)

        #seperate the ids into a list of all unowned items
        hat_ids = [hat.clothing_id for hat in response.context['hats_unowned']]
        shirt_ids = [shirt.clothing_id for shirt in response.context['shirts_unowned']]
        shoe_ids = [shoe.clothing_id for shoe in response.context['shoes_unowned']]

        #hat1 and shirt1 is owned by user
        self.assertNotIn(self.hat1.clothing_id, hat_ids)
        self.assertNotIn(self.shirt1.clothing_id, hat_ids)

        #other hats a shirt should be in the response
        self.assertIn(self.hat2.clothing_id, hat_ids)
        self.assertIn(self.shirt2.clothing_id, shirt_ids)
        self.assertIn(self.shoes1.clothing_id, shoe_ids)
        self.assertIn(self.shoes2.clothing_id, shoe_ids)

    def test_shop_all_clothing_owned(self):
        # Log in
        self.client.login(username="userAllClothes", password="testpass")
        # Get dress page
        response = self.client.get(reverse("shop_page"))
        self.assertEqual(response.status_code, 200)
    
        self.assertEqual(len(response.context['hats_unowned']), 0)
        self.assertEqual(len(response.context['shirts_unowned']), 0)
        self.assertEqual(len(response.context['shoes_unowned']), 0)

    def test_buy_clothing_all(self):
        """
        Considers the case where a user has purchased all of their clothing.

        Must return False.
        """
        # Log in 
        self.client.login(username="userAllClothes", password="testpass")
        # Get dress page
        response = self.client.get(reverse("shop_page"))
        self.assertEqual(response.status_code, 200)

        # Check purchase is possible
        self.assertEqual(self.fpuserAllClothes.buy_clothing(self.shirt1), False)

    def test_buy_clothing_cant_buy(self):
        """
        Considers the case where a user does not have enough coins to buy an 
        item.

        Must return False.
        """
        # Log in 
        self.client.login(username="userSomeClothes", password="testpass")
        # Get dress page
        response = self.client.get(reverse("shop_page"))
        self.assertEqual(response.status_code, 200)

        # Check purchase is possible
        self.assertEqual(self.fpuserSomeClothes.buy_clothing(self.shoes1), False)

    def test_buy_clothing_can_buy(self):
        """
        Considers the case where a user has enough coins to purchase an item.

        Must return True.
        """
        # Log in 
        self.client.login(username="userSomeClothes", password="testpass")
        # Get dress page
        response = self.client.get(reverse("shop_page"))
        self.assertEqual(response.status_code, 200)

        # Check purchase is possible
        self.assertEqual(self.fpuserSomeClothes.buy_clothing(self.hat1), True)


class DressPetTestCase(TestCase):
    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(username="user1", password="testpass")
        self.user2 = User.objects.create_user(username="user2", password="testpass")
        self.user3 = User.objects.create_user(username="user3", password="testpass")

        # Create FPUser instances
        self.fpuser1 = FPUser.objects.create(
            djuser=self.user1, username="user1", name="User One"
        )
        self.fpuser2 = FPUser.objects.create(
            djuser=self.user2, username="user2", name="User Two"
        )
        self.fpuser3 = FPUser.objects.create(
            djuser=self.user3, username="user3", name="User Three"
        )

        # Get clothing items
        clothing1 = Clothing.objects.get(clothing_id=1)  # hat1
        clothing2 = Clothing.objects.get(clothing_id=2)  # hat2
        clothing3 = Clothing.objects.get(clothing_id=3)  # shirt1
        clothing4 = Clothing.objects.get(clothing_id=4)  # shirt2
        clothing5 = Clothing.objects.get(clothing_id=5)  # shoes1
        clothing6 = Clothing.objects.get(clothing_id=6)  # shoes2

        # Assign clothing to users
        self.fpuser1.owns.add(
            clothing1, clothing2, clothing3, clothing4, clothing5, clothing6
        )
        self.fpuser2.owns.add(clothing1, clothing3, clothing5)

        # Create Pet instances
        self.pet1 = Pet.objects.create(
            owner=self.fpuser1, name="PetOne", image_path="images/test_pet.png"
        )
        self.pet2 = Pet.objects.create(
            owner=self.fpuser2, name="PetTwo", image_path="images/test_pet.png"
        )
        self.pet3 = Pet.objects.create(
            owner=self.fpuser3, name="PetThree", image_path="images/test_pet.png"
        )

    def test_1(self):
        # Log in
        self.client.login(username="user1", password="testpass")

        # Get dress page
        response = self.client.get(reverse("display_dress_page"))
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
        response = self.client.post(reverse("update_clothing"), {"clothing_id": 2})
        self.assertEqual(response.status_code, 200)

        # Refresh pet data
        self.pet1.refresh_from_db()
        self.assertEqual(self.pet1.hat.clothing_id, 2)

        # Change again
        response = self.client.post(
            reverse("update_clothing"), {"clothing_id": 1}  # Switching back to hat1
        )
        self.assertEqual(response.status_code, 200)
        self.pet1.refresh_from_db()
        self.assertEqual(self.pet1.hat.clothing_id, 1)

    def test_2(self):
        # Log in
        self.client.login(username="user2", password="testpass")

        # Get dress page
        response = self.client.get(reverse("display_dress_page"))
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
        response = self.client.post(reverse("update_clothing"), {"clothing_id": 1})
        self.assertEqual(response.status_code, 200)

        self.pet2.refresh_from_db()
        self.assertEqual(self.pet2.hat.clothing_id, 1)

        response = self.client.post(reverse("update_clothing"), {"clothing_id": 3})
        self.assertEqual(response.status_code, 200)

        self.pet2.refresh_from_db()
        self.assertEqual(self.pet2.shirt.clothing_id, 3)

    def test_3(self):
        # Log in
        self.client.login(username="user3", password="testpass")

        # Get dress page
        response = self.client.get(reverse("display_dress_page"))
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
    def setUp(self): ...

    def test_1(self): ...
