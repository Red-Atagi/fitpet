from django.shortcuts import render, redirect
from app.models import *
from django.http import JsonResponse
from .models import FPUser, Pet, Clothing
from .forms import CreateUserForm


def index(request):
    return render(request, 'base.html', {})


def display_dress_page(request):
    
    if not request.user.is_authenticated:
        return redirect('') # TODO: change this to login page
    user = request.user
    fpuser = FPUser.objects.filter(djuser = user)
    if (len(fpuser) != 1):
        return redirect('') # TODO: change this to login page
    
    hats_owned, shirts_owned, shoes_owned = fpuser.clothing_owned()
    
    pet = Pet.objects.filter(owner = fpuser)
    hat_wearing, shirt_wearing, shoes_wearing = pet.is_wearing()
    
    data = {
        "hats_owned": hats_owned,
        "shirts_owned": shirts_owned,
        "shoes_owned": shoes_owned,
        "hat_wearing": hat_wearing,
        "shirt_wearing": shirt_wearing,
        "shoes_wearing": shoes_wearing
    }
    
    return render(request, 'dress.html', data)


def change_clothing(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Invalid request method."})

    if not request.user.is_authenticated:
        return redirect('') # TODO: change this to login page

    try:
        new_clothing_id = int(request.POST.get('new_clothing_id'))
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
        pet.hat = clothing
    elif clothing.clothing_type == 'Shirt':
        pet.shirt = clothing
    elif clothing.clothing_type == 'Shoes':
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
