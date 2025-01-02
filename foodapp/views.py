from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def sign_up(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect('login') 
        else:
            messages.error(request, "Error creating account. Please try again.")
    else:
        form = UserCreationForm()

    return render(request, 'sign_up.html', {'form': form})



from django.shortcuts import render, redirect
from .models import Restaurant, MenuItem, Order, OrderItem

@login_required
def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    return render(request, "restaurant_list.html", {"restaurants": restaurants})

def menu_items(request, restaurant_id):
    menu = MenuItem.objects.filter(restaurant_id=restaurant_id)
    return render(request, "menu_items.html", {"menu": menu})

def cart(request):
    if "cart" not in request.session:
        request.session["cart"] = {}
    cart_items = request.session["cart"]

    items = []
    for item_id, qty in cart_items.items():
        try:
            menu_item = MenuItem.objects.get(id=item_id)
            items.append({"menu_item": menu_item, "quantity": qty})
        except MenuItem.DoesNotExist:
            messages.error(request, f"Menu item with ID {item_id} not found.")
    
    return render(request, "cart.html", {"items": items})


def add_to_cart(request, menu_item_id):
    if "cart" not in request.session:
        request.session["cart"] = {}
    cart = request.session["cart"]
    try:
        menu_item = MenuItem.objects.get(id=menu_item_id)
        cart[menu_item_id] = cart.get(menu_item_id, 0) + 1
        request.session.modified = True
        messages.success(request, f"{menu_item.name} added to cart.")
    except MenuItem.DoesNotExist:
        messages.error(request, "Item not found.")
    
    return redirect("cart")



def loginview(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Successfully logged in!")
                return redirect('restaurant_list')  
            else:
                messages.error(request, "Invalid credentials")
        else:
            messages.error(request, "Please enter both username and password")
    
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')


def sign_up(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')
        else:
            messages.error(request, "Invalid submission. Please check the errors below.")
    else:
        form = UserCreationForm()

    return render(request, 'sign_up.html', {'form': form})
