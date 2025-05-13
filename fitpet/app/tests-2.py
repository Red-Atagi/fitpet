from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from app.models import *
from .models import FPUser, Pet, Clothing, FriendRequest


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
        self.assertRedirects(response, reverse("friend_list"))

    def test_visit_friend_does_not_exist(self):
        """
        Test that visit friend redirects to home with a user who does not exist.
        """
        # Log in the user
        self.client.login(username="testuser", password="testpassword")

        # Try to visit a non-existent friend's page
        response = self.client.get(reverse("visit_friend", args=[9999]))

        # Check that the response redirects to the home page
        self.assertRedirects(response, reverse("friend_list"))


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


class CheckFriendRequestTestCase(TestCase):
    def setup(self):
        # Create a user and a pet for the tests
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.fpuser = FPUser.objects.create(
            djuser=self.user, coins=75, username="testuser", name="Test User"
        )
        self.pet = Pet.objects.create(name="Test Pet", owner=self.fpuser)

        # Create a friend user and pet for the tests
        self.friend_user = User.objects.create_user(
            username="frienduser", password="friendpass"
        )
        self.friend_fpuser = FPUser.objects.create(
            djuser=self.friend_user, coins=60, username="frienduser", name="Friend User"
        )
        self.friend_pet = Pet.objects.create(
            name="Friend Pet", owner=self.friend_fpuser
        )

    def test_leave_friend_page(self):
        """
        Test that leaves the friend list page
        """
        # Log In
        self.client.login(username="testuser", password="testpass")

        # Go to Friend Page
        response = self.client.get(reverse("friend_list"))
        self.assertEqual(response.status_code, 200)

        # Go Home
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_accept_friend_request(self):
        """
        Test that accepts a friend request and adds friends to the users
        """
        # Log In
        self.client.login(username="testuser", password="testpass")

        # Go to Friend Page
        response = self.client.get(reverse("friend_list"))
        self.assertEqual(response.status_code, 200)

        # Go to Friend Request Page
        response = self.client.get(reverse("friend_request"))
        self.assertEqual(response.status_code, 200)

        # Accept Friend Request
        answer = 1
        friend = self.friend_fpuser.user_id
        response = self.client.post(
            reverse("friend_request"), {"answer": answer, "friend": friend}
        )
        # Add Friend to Friend :ist
        self.fpuser.friends.add(self.friend_fpuser)
        self.friend_fpuser.friends.add(self.fpuser)

        self.assertContains(self.fpuser.friends, self.friend_fpuser)
        self.assertContains(self.friend_fpuser.friends, self.fpuser)
        # Remove friend from friend request
        """
        Need to create a method for the friend requests to be 
        sent / seen in the backend
        """

        # Go to Friend Page
        response = self.client.get(reverse("friend_list"))
        self.assertEqual(response.status_code, 200)

        # Go Home
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_decline_friend_request(self):
        """
        Test that declines the friend request
        """
        # Log In
        self.client.login(username="testuser", password="testpass")

        # Go to Friend Page
        response = self.client.get(reverse("friend_list"))
        self.assertEqual(response.status_code, 200)

        # Go to Friend Request Page
        response = self.client.get(reverse("friend_request"))
        self.assertEqual(response.status_code, 200)

        # Decline Friend Request
        answer = 0
        friend = self.friend_fpuser.user_id
        response = self.client.post(
            reverse("friend_request"), {"answer": answer, "friend": friend}
        )

        # Remove friend from friend request
        """
        Need to create a method for the friend requests to be 
        sent / seen in the backend
        """

        # Go to Friend Page
        response = self.client.get(reverse("friend_list"))
        self.assertEqual(response.status_code, 200)
        # Go Home
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)


class FriendRequestTests(TestCase):
    def setUp(self):
        # Create two users and their FPUser profiles
        self.user1 = User.objects.create_user(username="alice", password="pass1234")
        self.user2 = User.objects.create_user(username="bob", password="pass1234")
        self.fp1 = FPUser.objects.create(
            djuser=self.user1, username="alice", name="Alice"
        )
        self.fp2 = FPUser.objects.create(djuser=self.user2, username="bob", name="Bob")

        self.client = Client()
        self.client.login(username="alice", password="pass1234")

    def test_create_friend_request_model(self):
        """Creating a friend request between users should work"""
        FriendRequest.objects.create(from_user=self.fp1, to_user=self.fp2)
        req = FriendRequest.objects.get(from_user=self.fp1, to_user=self.fp2)
        self.assertEqual(req.from_user.username, "alice")
        self.assertEqual(req.to_user.username, "bob")

    def test_duplicate_friend_request_not_allowed(self):
        """Duplicate friend requests should raise an error"""
        FriendRequest.objects.create(from_user=self.fp1, to_user=self.fp2)
        with self.assertRaises(Exception):
            FriendRequest.objects.create(from_user=self.fp1, to_user=self.fp2)

    def test_search_users_view_returns_results(self):
        """Searching by username should return matching users"""
        response = self.client.post("/search_users/", {"query": "bo"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "bob")

    def test_search_users_does_not_return_self(self):
        """Search should not return the current user"""
        response = self.client.post("/search_users/", {"query": "ali"})
        self.assertNotContains(response, "alice")

    def test_send_friend_request_view_creates_request(self):
        """GET to send_request URL should create a FriendRequest"""
        response = self.client.get(f"/send_request/{self.fp2.user_id}/")
        self.assertEqual(response.status_code, 302)  # redirect expected
        self.assertTrue(
            FriendRequest.objects.filter(from_user=self.fp1, to_user=self.fp2).exists()
        )

    def test_cannot_send_request_to_self(self):
        """Sending a request to self should do nothing"""
        response = self.client.get(f"/send_request/{self.fp1.user_id}/")
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            FriendRequest.objects.filter(from_user=self.fp1, to_user=self.fp1).exists()
        )


class FriendRequestTests(TestCase):

    def setUp(self):
        # Create two users and their FPUser profiles
        self.user1 = User.objects.create_user(username="alice", password="pass1234")
        self.user2 = User.objects.create_user(username="bob", password="pass1234")

        self.fp1 = FPUser.objects.create(
            djuser=self.user1, username="alice", name="Alice"
        )

        self.fp2 = FPUser.objects.create(djuser=self.user2, username="bob", name="Bob")

        self.client = Client()

        self.client.login(username="alice", password="pass1234")

    def test_create_friend_request_model(self):
        """Creating a friend request between users should work"""

        FriendRequest.objects.create(from_user=self.fp1, to_user=self.fp2)

        req = FriendRequest.objects.get(from_user=self.fp1, to_user=self.fp2)

        self.assertEqual(req.from_user.username, "alice")

        self.assertEqual(req.to_user.username, "bob")

    def test_accept_friend_request(self):
        """Accepting a friend request should add the users as friends"""

        FriendRequest.objects.create(from_user=self.fp2, to_user=self.fp1)

        response = self.client.post(
            f"/respond_request/{self.fp2.user_id}/", {"action": "accept"}
        )

        self.assertEqual(response.status_code, 302)

        self.assertIn(self.fp2, self.fp1.friends.all())

    def test_decline_friend_request(self):
        """Declining a friend request should remove it"""

        FriendRequest.objects.create(from_user=self.fp2, to_user=self.fp1)

        response = self.client.post(
            f"/respond_request/{self.fp2.user_id}/", {"action": "decline"}
        )

        self.assertFalse(
            FriendRequest.objects.filter(from_user=self.fp2, to_user=self.fp1).exists()
        )

    def test_cannot_accept_others_request(self):
        """User should not be able to accept a request sent to another user"""

        FriendRequest.objects.create(from_user=self.fp1, to_user=self.fp2)

        response = self.client.post(
            f"/respond_request/{self.fp1.user_id}/", {"action": "accept"}
        )

        self.assertEqual(response.status_code, 403)

    def test_duplicate_friend_request_not_allowed(self):
        """Duplicate friend requests should raise an error"""

        FriendRequest.objects.create(from_user=self.fp1, to_user=self.fp2)

        with self.assertRaises(Exception):

            FriendRequest.objects.create(from_user=self.fp1, to_user=self.fp2)

    def test_search_users_view_returns_results(self):
        """Searching by username should return matching users"""

        response = self.client.post("/search_users/", {"query": "bo"})

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "bob")

    def test_search_users_does_not_return_self(self):
        """Search should not return the current user"""

        response = self.client.post("/search_users/", {"query": "ali"})

        self.assertNotContains(response, "alice")

    def test_send_friend_request_view_creates_request(self):
        """GET to send_request URL should create a FriendRequest"""

        response = self.client.get(f"/send_request/{self.fp2.user_id}/")

        self.assertEqual(response.status_code, 302)  # redirect expected

        self.assertTrue(
            FriendRequest.objects.filter(from_user=self.fp1, to_user=self.fp2).exists()
        )

    def test_cannot_send_request_to_self(self):
        """Sending a request to self should do nothing"""

        response = self.client.get(f"/send_request/{self.fp1.user_id}/")

        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            FriendRequest.objects.filter(from_user=self.fp1, to_user=self.fp1).exists()
        )

    def test_accept_invalid_request_fails(self):
        """Accepting a non-existent request should return 404"""

        response = self.client.post(
            f"/respond_request/{self.fp2.user_id}/", {"action": "accept"}
        )

        self.assertEqual(response.status_code, 404)
