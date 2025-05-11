from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from app.models import *
from .models import FPUser, Pet, Clothing


class VisitFriendTestCase(TestCase):
    def setUp(self):
        # Create a user and a pet for the test
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.fpuser = FPUser.objects.create(
            djuser=self.user, coins=100, username="testuser", name="Test User"
        )
        self.pet = Pet.objects.create(name="Test Pet", owner=self.fpuser)

        # Create a friend user and pet
        self.friend_user = User.objects.create_user(
            username="frienduser", password="friendpassword"
        )
        self.friend_fpuser = FPUser.objects.create(
            djuser=self.friend_user, coins=50, username="frienduser", name="Friend User"
        )
        self.friend_pet = Pet.objects.create(
            name="Friend Pet", owner=self.friend_fpuser
        )

        # Add the friend
        self.fpuser.friends.add(self.friend_fpuser)
        self.friend_fpuser.friends.add(self.fpuser)

    def test_visit_friend_page(self):
        """
        Test that visit friend works with correct friend and pet.
        """
        # Log in the user
        self.client.login(username="testuser", password="testpassword")

        # Visit the friend's page
        response = self.client.get(
            reverse("visit_friend", args=[self.friend_fpuser.user_id])
        )

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check that the friend is actually the one we expect
        friend = response.context["friend"]
        self.assertEqual(friend.user_id, self.friend_fpuser.user_id)

        # Check that the pet is actually the one we expect
        pet = response.context["pet"]
        self.assertEqual(pet.pet_id, self.friend_pet.pet_id)

    def test_visit_friend_page_not_friend(self):
        """
        Test that visit friend redirects to home with a user who is not a friend.
        """
        # Create a new user and pet who is not a friend
        new_user = User.objects.create_user(
            username="notFriend", password="testpassword"
        )
        new_fpuser = FPUser.objects.create(
            djuser=new_user, coins=50, username="notFriend", name="New User"
        )
        new_pet = Pet.objects.create(name="Not Friend Pet", owner=new_fpuser)

        # Log in the user
        self.client.login(username="testuser", password="testpassword")

        # Try to visit the friend's page
        response = self.client.get(reverse("visit_friend", args=[new_fpuser.user_id]))

        # Check that the response redirects to the home page
        self.assertRedirects(response, reverse("home"))

    def test_visit_friend_does_not_exist(self):
        """
        Test that visit friend redirects to home with a user who does not exist.
        """
        # Log in the user
        self.client.login(username="testuser", password="testpassword")

        # Try to visit a non-existent friend's page
        response = self.client.get(reverse("visit_friend", args=[9999]))

        # Check that the response redirects to the home page
        self.assertRedirects(response, reverse("home"))


class FriendListTestCase(TestCase):
    def setUp(self):
        # Create a user and a pet for the test
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.fpuser = FPUser.objects.create(
            djuser=self.user, coins=100, username="testuser", name="Test User"
        )
        self.pet = Pet.objects.create(name="Test Pet", owner=self.fpuser)

        # Create a friend user and pet
        self.friend_user = User.objects.create_user(
            username="frienduser", password="friendpassword"
        )
        self.friend_fpuser = FPUser.objects.create(
            djuser=self.friend_user, coins=50, username="frienduser", name="Friend User"
        )
        self.friend_pet = Pet.objects.create(
            name="Friend Pet", owner=self.friend_fpuser
        )

        # Create second friend user and pet
        self.friend_user2 = User.objects.create_user(
            username="friend2user", password="friendpassword"
        )
        self.friend_fpuser2 = FPUser.objects.create(
            djuser=self.friend_user,
            coins=50,
            username="friend2user",
            name="Friend User",
        )
        self.friend_pet2 = Pet.objects.create(
            name="Friend Pet", owner=self.friend_fpuser
        )

        # Add the friend 1
        self.fpuser.friends.add(self.friend_fpuser)
        self.friend_fpuser.friends.add(self.fpuser)

        # Add the friend 2
        self.fpuser.friends.add(self.friend_fpuser2)
        self.friend_fpuser2.friends.add(self.fpuser)

    def test_visit_friend_page(self):
        """
        Test that visit friend works with correct friend and pet.
        """
        # Log in the user
        self.client.login(username="testuser", password="testpassword")

        # Visit the friend's page
        response = self.client.get(reverse("friend_list"))

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

        friends = response.context["friends"]

        # Check that there are 2 friends
        self.assertEqual(len(friends), 2)

        # Check that the friends are the right ones
        self.assertIn(self.friend_fpuser, friends)
        self.assertIn(self.friend_fpuser2, friends)

    def test_visit_friend_page_no_friends(self):
        """
        Tests that no friendse are shown when the user has no friends.
        """
        # Create a new user and pet who has no a friend
        new_user = User.objects.create_user(
            username="notFriend", password="testpassword"
        )
        new_fpuser = FPUser.objects.create(
            djuser=new_user, coins=50, username="notFriend", name="New User"
        )
        new_pet = Pet.objects.create(name="Not Friend Pet", owner=new_fpuser)

        # Log in the user
        self.client.login(username="notFriend", password="testpassword")

        # Try to visit the friend's page
        response = self.client.get(reverse("friend_list"))

        # Check that the response is ok (200)
        self.assertEqual(response.status_code, 200)

        friends = response.context["friends"]

        # Check that there are 0 friends
        self.assertEqual(len(friends), 0)
