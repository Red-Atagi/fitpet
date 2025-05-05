from django.shortcuts import render, redirect
from app.models import *
from django.http import JsonResponse
from .models import FPUser, Pet, Clothing
from .forms import CreateUserForm

import logging
logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'base.html', {})


def display_dress_page(request):
    
    if not request.user.is_authenticated:
        return redirect('login') 
    user = request.user

    try:
        fpuser = FPUser.objects.get(djuser=user)
    
    except FPUser.DoesNotExist:
        fpuser = FPUser.objects.create(
            djuser=user,
            username=user.username,
            name=user.get_full_name() or user.username,
            coins=0
        )
        # Optionally, assign default clothing items if needed
        # Example: give them all clothing with "starter" tag
        # Get clothing items
        clothing1 = Clothing.objects.get(clothing_id=1)  # hat1
        clothing2 = Clothing.objects.get(clothing_id=2)  # hat2
        clothing3 = Clothing.objects.get(clothing_id=3)  # shirt1
        clothing4 = Clothing.objects.get(clothing_id=4)  # shirt2
        clothing5 = Clothing.objects.get(clothing_id=5)  # shoes1
        clothing6 = Clothing.objects.get(clothing_id=6)  # shoes2
        clothing7 = Clothing.objects.get(clothing_id=7)  # shoes3
        clothing8 = Clothing.objects.get(clothing_id=8)  # shoes4
        clothing9 = Clothing.objects.get(clothing_id=9)  # shoes5

        # Assign clothing to users
        fpuser.owns.add(clothing1, clothing2, clothing3, clothing4, clothing5, clothing6, clothing7, clothing8, clothing9)

        pet1 = Pet.objects.create(
            owner=fpuser, name="PetOne", image_path="images/test_pet.png", hat=clothing1
        )
    
        return redirect('login')  

    hats_owned, shirts_owned, shoes_owned = fpuser.clothing_owned()
    
    pet = Pet.objects.get(owner=fpuser)

    logger.debug(f"Pet hat: {pet.hat}")  # Log the pet's hat to check if it's being fetched correctly
    logger.debug(f"Hat wearing: {pet.hat}")  # Log the hat that the pet is wearing (or check other attributes)

    hat_wearing, shirt_wearing, shoes_wearing = pet.is_wearing()

    clothing_lists = [hats_owned, shirts_owned, shoes_owned]
    currently_wearing = [hat_wearing, shirt_wearing, shoes_wearing]


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
        "hat_wearing": hat_wearing,
        "shirt_wearing": shirt_wearing,
        "shoes_wearing": shoes_wearing
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
        return redirect('') # TODO: change this to login page
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
            userFP = FPUser.objects.create(
                ## User_id is automatically generated
                djuser = user,
                username = user.username,
                ## Can set name changing capabilities later
                name = "",
                coins = 0
            )
            Pet.objects.create(
            ## Can set name changing capabilities later
            name = "",
            xp=0,
            owner = userFP
            )
            ## After successful account creation, return to main page
            return redirect('index')
    else:
        form = CreateUserForm()
    return render(request, 'register.html', {'form': form})
