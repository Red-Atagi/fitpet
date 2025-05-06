import json
import os
from django.conf import settings
from django.shortcuts import render, redirect
from app.models import *
from django.http import JsonResponse
from .models import FPUser, Pet, Clothing, Exercise
from .forms import CreateUserForm

import logging
logger = logging.getLogger(__name__)


# def index(request):
#     return render(request, 'base.html', {})

def display_home_page(request):
    
    if not request.user.is_authenticated:
        return redirect('login') 
    user = request.user

    try:
        fpuser = FPUser.objects.get(djuser=user)
    
    except FPUser.DoesNotExist:
        return redirect('login')  
    
    pet = Pet.objects.get(owner=fpuser)

    hat_wearing, shirt_wearing, shoes_wearing, background_wearing = pet.is_wearing()
    
    data = {
        "hat_wearing": hat_wearing,
        "shirt_wearing": shirt_wearing,
        "shoes_wearing": shoes_wearing,
        "background_wearing": background_wearing,
    }
    
    return render(request, 'base.html', data)


def display_dress_page(request):
    
    if not request.user.is_authenticated:
        return redirect('login') 
    user = request.user 

    try:
        fpuser = FPUser.objects.get(djuser=user)
    
    except FPUser.DoesNotExist:
        return redirect('login')  

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
    
    return render(request, 'dress.html', data)


def update_clothing(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Invalid request method."})

    if not request.user.is_authenticated:
        return redirect('login') 

    try:
        new_clothing_id = int(request.POST.get('clothing_id'))
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
    if clothing.clothing_type == 'Hat':
        if pet.hat and pet.hat.clothing_id == clothing.clothing_id:
            pet.hat = None
        else: 
            pet.hat = clothing
    elif clothing.clothing_type == 'Shirt':
        if pet.shirt and pet.shirt.clothing_id == clothing.clothing_id:
            pet.shirt = None
        else: 
            pet.shirt = clothing
    elif clothing.clothing_type == 'Shoes':
        if pet.shoes and pet.shoes.clothing_id == clothing.clothing_id:
            pet.shoes = None
        else: 
            pet.shoes = clothing
    elif clothing.clothing_type == 'Background':
        if pet.background and pet.background.clothing_id == clothing.clothing_id:
            pet.background = None
        else: 
            pet.background = clothing

    pet.save()

    # Return the success response with updated pet image or other details
    return JsonResponse({
        'success': True,
        'new_image_url': pet.image_path,  # Assuming you want to return the pet's image path
    })


def shop_page(request):
    """
    Renders the shop page with the items the user does not own.
    """
    if not request.user.is_authenticated:
        unowned_clothing = Clothing.objects.all()
        hats = unowned_clothing.filter(clothing_type="Hat")
        shirts = unowned_clothing.filter(clothing_type="Shirt")
        shoes = unowned_clothing.filter(clothing_type="Shoes")
        data = {
            "hats_unowned": hats,
            "shirts_unowned": shirts,
            "shoes_unowned": shoes,
            "user": None
        }
        return render(request, 'shop.html', data)
    user = request.user
    fpuser = FPUser.objects.get(djuser=user)

    owned_clothing = fpuser.owns.all()
    unowned_clothing = Clothing.objects.exclude(clothing_id__in=owned_clothing.values_list('clothing_id', flat=True))
    
    hats = unowned_clothing.filter(clothing_type="Hat")
    shirts = unowned_clothing.filter(clothing_type="Shirt")
    shoes = unowned_clothing.filter(clothing_type="Shoes")

    pet = Pet.objects.filter(owner = fpuser)
    # hat_wearing, shirt_wearing, shoes_wearing = pet.is_wearing()

    data = {
        "hats_unowned": hats,
        "shirts_unowned": shirts,
        "shoes_unowned": shoes,
        "user": user,
        "pet": pet
        # "hat_wearing": hat_wearing,
        # "shirt_wearing": shirt_wearing,
        # "shoes_wearing": shoes_wearing
    }
    
    return render(request, 'shop.html', data)

def buy_clothing(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Invalid request method."})

    if not request.user.is_authenticated:
        return redirect('login') 

    try:
        new_clothing_id = int(request.POST.get('clothing_id'))
    except (TypeError, ValueError):
        return JsonResponse({"success": False, "error": "Invalid clothing ID."})
    
    # Get the FPUser
    fpuser = FPUser.objects.filter(djuser=request.user).first()
    if not fpuser:
        return JsonResponse({"success": False, "error": "User profile not found."})
    
    if fpuser.buy_clothing(Clothing.objects.filter(clothin_id=new_clothing_id).first()):
        return JsonResponse({
            'success': True,
        })
    return JsonResponse({"success": False, "error": "Failed to buy clothes"})


def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        ## Django already has capabilities checking if username and password work
        if form.is_valid():
            ## Use Django capabilities to save information of the User
            user = form.save()
            name = form.cleaned_data.get('name')
            pet_name = form.cleaned_data.get('pet_name')
            userFP = FPUser.objects.create(
                ## User_id is automatically generated
                djuser = user,
                username = user.username,
                ## Can set name changing capabilities later
                name = name,
                coins = 0
            )
            Pet.objects.create(
            ## Can set name changing capabilities later
            name = pet_name,
            xp=0,
            owner = userFP
            )
            ## After successful account creation, return to main page
            return redirect('home')
    else:
        form = CreateUserForm()
    return render(request, 'register.html', {'form': form})

def load_exercises():
    """
    Loads all of the exercises into a list from the exercise json file
    """
    path = os.path.join(settings.BASE_DIR, 'app', 'data', 'exercise.json')
    with open(path, 'r') as file:
        data = json.load(file)

    return data


def workout_page(request):

    if not request.user.is_authenticated:
        redirect('login')

    exercises = load_exercises()
    return render(request, 'workout.html',{'exercises': exercises})

def findExercise(name):
    exercises = load_exercises()
    for exercise in exercises:
        if exercise['exercise'] == name:
            return Exercise(
                name = exercise['exercise'],
                tier = int(exercise['tier']),
                max_reps = int(exercise['max_reps'])
            )
    return None

def log_workout(request):
    if not request.user.is_authenticated:
        redirect ('login')
    if request.method == 'POST':
        """
        # Get the fpuser
        user = request.user
        fpuser = FPUser.objects.get(djuser = user)
        # Get the Pet of the Fpuser
        pet = Pet.objects.filter(owner = fpuser)
        """
        # Get the amount of reps done, max_reps, level /tier of exercise
        reps = int(request.POST.get('reps'))
        name = request.POST.get('exercise')
        
        CurrentExercise = findExercise(name)

        
        gainedXP = CurrentExercise.calculateXP(reps)
        gainedCoins = CurrentExercise.calculateCoins(reps)
        #canLevelUp = gainedXP >= pet.neededXP 
        """
        user.addCoins(gainedCoins)
        pet.addXP(gainedXP)
        """
            # add the coins and xp to the user and the pet
            

        return render(request, 'logged_workout.html', {
            'gainedXP': gainedXP,
            'gainedCoins': gainedCoins,
            #'leveled_up' : canLevelUp
            'exercises': load_exercises()
        })
