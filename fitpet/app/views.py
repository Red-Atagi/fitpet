import json
import os
from django.conf import settings
from django.shortcuts import render, redirect
from app.models import *
from django.http import JsonResponse
from .models import FPUser, Pet, Clothing, Exercise, FriendRequest
from .forms import CreateUserForm, UserSearchForm

import logging

logger = logging.getLogger(__name__)


# def index(request):
#     return render(request, 'base.html', {})


def display_home_page(request):

    if not request.user.is_authenticated:
        return redirect("login")
    user = request.user

    try:
        fpuser = FPUser.objects.get(djuser=user)

    except FPUser.DoesNotExist:
        return redirect("login")

    pet = Pet.objects.get(owner=fpuser)

    hat_wearing, shirt_wearing, shoes_wearing, background_wearing = pet.is_wearing()

    data = {
        "hat_wearing": hat_wearing,
        "shirt_wearing": shirt_wearing,
        "shoes_wearing": shoes_wearing,
        "background_wearing": background_wearing,
    }

    return render(request, "base.html", data)


def display_dress_page(request):

    if not request.user.is_authenticated:
        return redirect("login")
    user = request.user

    try:
        fpuser = FPUser.objects.get(djuser=user)

    except FPUser.DoesNotExist:
        return redirect("login")

    hats_owned, shirts_owned, shoes_owned, backgrounds_owned = fpuser.clothing_owned()

    pet = Pet.objects.get(owner=fpuser)

    hat_wearing, shirt_wearing, shoes_wearing, background_wearing = pet.is_wearing()

    clothing_lists = [hats_owned, shirts_owned, shoes_owned, backgrounds_owned]
    currently_wearing = [hat_wearing, shirt_wearing, shoes_wearing, background_wearing]

    # # Sort the list so that the item currently worn is at the head
    for i in range(len(clothing_lists)):
        clothing_list = clothing_lists[i]
        wearing_item = currently_wearing[i]

        for idx, item in enumerate(clothing_list):
            if wearing_item and item.clothing_id == wearing_item.clothing_id:
                clothing_list.insert(0, clothing_list.pop(idx))
                break

    data = {
        "hats_owned": hats_owned,
        "shirts_owned": shirts_owned,
        "shoes_owned": shoes_owned,
        "backgrounds_owned": backgrounds_owned,
        "hat_wearing": hat_wearing,
        "shirt_wearing": shirt_wearing,
        "shoes_wearing": shoes_wearing,
        "background_wearing": background_wearing,
    }

    return render(request, "dress.html", data)


def update_clothing(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Invalid request method."})

    if not request.user.is_authenticated:
        return redirect("login")

    try:
        new_clothing_id = int(request.POST.get("clothing_id"))
    except (TypeError, ValueError):
        return JsonResponse({"success": False, "error": "Invalid clothing ID."})

    # Get the FPUser
    fpuser = FPUser.objects.filter(djuser=request.user).first()
    if not fpuser:
        return JsonResponse({"success": False, "error": "User profile not found."})

    # Get the Pet
    pet = Pet.objects.filter(owner=fpuser).first()
    if not pet:
        return JsonResponse({"success": False, "error": "Pet not found."})

    # Update the pet's clothing based on the type
    clothing = Clothing.objects.get(clothing_id=new_clothing_id)
    if clothing.clothing_type == "Hat":
        if pet.hat and pet.hat.clothing_id == clothing.clothing_id:
            pet.hat = None
        else:
            pet.hat = clothing
    elif clothing.clothing_type == "Shirt":
        if pet.shirt and pet.shirt.clothing_id == clothing.clothing_id:
            pet.shirt = None
        else:
            pet.shirt = clothing
    elif clothing.clothing_type == "Shoes":
        if pet.shoes and pet.shoes.clothing_id == clothing.clothing_id:
            pet.shoes = None
        else:
            pet.shoes = clothing
    elif clothing.clothing_type == "Background":
        if pet.background and pet.background.clothing_id == clothing.clothing_id:
            pet.background = None
        else:
            pet.background = clothing

    pet.save()

    # Return the success response with updated pet image or other details
    return JsonResponse(
        {
            "success": True,
            "new_image_url": pet.image_path,  # Assuming you want to return the pet's image path
        }
    )


def friend_list(request):
    """
    Renders the friend list page with the user's friends.
    """
    if not request.user.is_authenticated:
        return redirect("login")

    user = request.user
    fpuser = FPUser.objects.get(djuser=user)

    friends = fpuser.friends.all()

    data = {
        "friends": friends,
        "user": user,
    }

    return render(request, "friend_list.html", data)


def visit_friend(request, friend_id):
    """
    Renders the friend's page with the friends pet.
    """
    if not request.user.is_authenticated:
        return redirect("login")

    user = request.user
    fpuser = FPUser.objects.get(djuser=user)

    # try to get the user with id friend_id
    try:
        friend = FPUser.objects.get(user_id=friend_id)
    except FPUser.DoesNotExist:
        return redirect("friend_list")

    # # Check if the friend is actially a friend
    if not fpuser.friends.filter(user_id=friend_id).exists():
        return redirect("friend_list")

    pet = Pet.objects.filter(owner=friend).first()

    if not pet:
        return redirect("home")
    
    hats_owned, shirts_owned, shoes_owned, backgrounds_owned = friend.clothing_owned()
    hat_wearing, shirt_wearing, shoes_wearing, background_wearing = pet.is_wearing()

    clothing_lists = [hats_owned, shirts_owned, shoes_owned, backgrounds_owned]
    currently_wearing = [hat_wearing, shirt_wearing, shoes_wearing, background_wearing]

    # # Sort the list so that the item currently worn is at the head
    for i in range(len(clothing_lists)):
        clothing_list = clothing_lists[i]
        wearing_item = currently_wearing[i]

        for idx, item in enumerate(clothing_list):
            if wearing_item and item.clothing_id == wearing_item.clothing_id:
                clothing_list.insert(0, clothing_list.pop(idx))
                break
    # friend.user_id
    friends = friend.friends.all()

    data = {
        "friend": friend,
        "friends": friends,
        "pet": pet,
        "user": user,
        "hats_owned": hats_owned,
        "shirts_owned": shirts_owned,
        "shoes_owned": shoes_owned,
        "backgrounds_owned": backgrounds_owned,
        "hat_wearing": hat_wearing,
        "shirt_wearing": shirt_wearing,
        "shoes_wearing": shoes_wearing,
        "background_wearing": background_wearing,
    }

    return render(request, "friend.html", data)

def view_friend_requests(request):
    """
    Renders the friend request list page with the requests sent to the user.
    """

    if not request.user.is_authenticated:
        return redirect("login")
    
    # Get the fpuser
    user = request.user
    fpuser = FPUser.objects.get(djuser=user)

    # Get all friend requests that were sent to the user
    friend_requests = FriendRequest.objects.filter(to_user= fpuser).all()

    data = {
        "friend_requests" : friend_requests,
    }

    return render(request, "friend_request.html", data)

def confirm_friend_request(request, action, from_user_id):
    """
    Handles acceptance or denial of friend request
    """
    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == "POST":
        try:
            # Get the friend's fpuser
            from_user = FPUser.objects.get(user_id = from_user_id)

            # Get the current user's fpuser
            user = request.user
            to_user = FPUser.objects.get(djuser = user)

            # Get the friend request
            friend_request = FriendRequest.objects.get(from_user = from_user, to_user = to_user)
        except:
            return redirect("friend_request")
        
        # If the user accepts the friend request it adds to friends list
        if action == 'accept':
            to_user.friends.add(from_user)
            from_user.friends.add(to_user)
            to_user.save()
            from_user.save()

        # delete this friend request
        friend_request.delete()
        return redirect("friend_request")
    
    return redirect("friend_request")



def shop_page(request):
    """
    Renders the shop page with the items the user does not own.
    """
    if not request.user.is_authenticated:
        unowned_clothing = Clothing.objects.all()
        hats = unowned_clothing.filter(clothing_type="Hat")
        shirts = unowned_clothing.filter(clothing_type="Shirt")
        shoes = unowned_clothing.filter(clothing_type="Shoes")
        backgrounds = unowned_clothing.filter(clothing_type="Background")
        
        data = {
            "hats_unowned": hats,
            "shirts_unowned": shirts,
            "shoes_unowned": shoes,
            "backgrounds_unowned": backgrounds,
            "user": None,
        }
        return render(request, "shop.html", data)
    user = request.user
    fpuser = FPUser.objects.get(djuser=user)

    owned_clothing = fpuser.owns.all()
    unowned_clothing = Clothing.objects.exclude(
        clothing_id__in=owned_clothing.values_list("clothing_id", flat=True)
    )

    hats = unowned_clothing.filter(clothing_type="Hat")
    shirts = unowned_clothing.filter(clothing_type="Shirt")
    shoes = unowned_clothing.filter(clothing_type="Shoes")
    backgrounds = unowned_clothing.filter(clothing_type="Background")


    pet = Pet.objects.filter(owner=fpuser)
    # hat_wearing, shirt_wearing, shoes_wearing = pet.is_wearing()

    data = {
        "hats_unowned": hats,
        "shirts_unowned": shirts,
        "shoes_unowned": shoes,
        "user": fpuser,
        "pet": pet,
        "backgrounds_unowned": backgrounds,
        # "hat_wearing": hat_wearing,
        # "shirt_wearing": shirt_wearing,
        # "shoes_wearing": shoes_wearing
    }

    return render(request, "shop.html", data)


def buy_clothing(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Invalid request method."})

    if not request.user.is_authenticated:
        return redirect("login")

    try:
        new_clothing_id = int(request.POST.get("clothing_id"))
    except (TypeError, ValueError):
        return JsonResponse({"success": False, "error": "Invalid clothing ID."})

    # Get the FPUser
    fpuser = FPUser.objects.filter(djuser=request.user).first()
    if not fpuser:
        return JsonResponse({"success": False, "error": "User profile not found."})

    if fpuser.buy_clothing(
        Clothing.objects.filter(clothing_id=new_clothing_id).first()
    ):
        fpuser.save()
        return JsonResponse(
            {
                "success": True,
            }
        )
    return JsonResponse({"success": False, "error": "Failed to buy clothes"})


def register(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        ## Django already has capabilities checking if username and password work
        if form.is_valid():
            ## Use Django capabilities to save information of the User
            user = form.save()
            name = form.cleaned_data.get("name")
            pet_name = form.cleaned_data.get("pet_name")
            userFP = FPUser.objects.create(
                ## User_id is automatically generated
                djuser=user,
                username=user.username,
                ## Can set name changing capabilities later
                name=name,
                coins=0,
            )
            Pet.objects.create(
                ## Can set name changing capabilities later
                name=pet_name,
                xp=0,
                owner=userFP,
            )
            ## After successful account creation, return to main page
            return redirect("home")
    else:
        form = CreateUserForm()
    return render(request, "register.html", {"form": form})


def load_exercises():
    """
    Loads all of the exercises into a list from the exercise json file
    """
    path = os.path.join(settings.BASE_DIR, "app", "data", "exercise.json")
    with open(path, "r") as file:
        data = json.load(file)

    return data


def workout_page(request):

    if not request.user.is_authenticated:
        return redirect("login")

    return render(request, "workout.html", {"exercises": load_exercises()})


def findExercise(name):
    exercises = load_exercises()
    for exercise in exercises:
        if exercise["name"] == name:
            return Exercise(
                name=exercise["name"],
                tier=int(exercise["tier"]),
                max_reps=int(exercise["max_reps"]),
            )
    return None


def log_workout(request):

    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == "POST":

        # Get the fpuser
        user = request.user
        fpuser = FPUser.objects.get(djuser=user)
        # Get the Pet of the Fpuser
        pet = Pet.objects.filter(owner=fpuser).first()

        # Get the amount of reps done, max_reps, level /tier of exercise
        reps = int(request.POST.get("reps"))
        name = request.POST.get("exercise")

        CurrentExercise = findExercise(name)

        # calculate XP, coins, and if the pet has leveled up
        gainedXP = CurrentExercise.calculateXP(reps)
        gainedCoins = CurrentExercise.calculateCoins(reps)
        canLevelUp = gainedXP >= pet.neededXP()

        # Add the coins and XP to the user and pet
        fpuser.addCoins(gainedCoins)
        pet.addXP(gainedXP)

        fpuser.save()
        pet.save()

        return render(
            request,
            "logged_workout.html",
            {
                "gainedXP": gainedXP,
                "gainedCoins": gainedCoins,
                "leveled_up": canLevelUp,
            },
        )

def friend_list(request):
    """
    Renders the friend list page with the user's friends.
    """
    if not request.user.is_authenticated:
        return redirect("login")

    user = request.user
    fpuser = FPUser.objects.get(djuser=user)

    friends = fpuser.friends.all()

    return render(request, "friend_list.html", {
        "friends": friends,
        "fpuser": fpuser,
    })

def search_users(request):
    """
    Search for users to send a friend request to.
    """
    if not request.user.is_authenticated:
        return redirect("login")

    fpuser = FPUser.objects.get(djuser=request.user)
    results = []

    if request.method == "POST":
        form = UserSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = FPUser.objects.filter(username__icontains=query) \
            .exclude(user_id=fpuser.user_id) \
            .exclude(user_id__in=fpuser.friends.values_list('user_id', flat=True))
    else:
        form = UserSearchForm()

    return render(request, "search_users.html", {
        "form": form,
        "results": results,
        "fpuser": fpuser,
    })


def send_friend_request(request, to_user_id):
    """
    Sends a friend request from the logged-in user to another FPUser.
    """
    if not request.user.is_authenticated:
        return redirect("login")

    from_user = FPUser.objects.get(djuser=request.user)
    to_user = FPUser.objects.get(user_id=to_user_id)

    if from_user != to_user:
        # Avoid duplicate requests
        already_exists = FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists()
        if not already_exists:
            FriendRequest.objects.create(from_user=from_user, to_user=to_user)
            print(f"Request sent from {from_user.username} to {to_user.username}")
        else:
            print("Friend request already exists.")
    else:
        print("Cannot send request to yourself.")

    return redirect("search_users")
