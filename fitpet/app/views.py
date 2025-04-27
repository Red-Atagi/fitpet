from django.shortcuts import render, redirect
from app.models import *
from django.http import JsonResponse

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