import uuid 
import requests 
import json 

from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q 
from django.core.paginator import Paginator
from . models import *
from .forms import *

# Create your views here.


def index(request):
    category = Category.objects.all().order_by("id")
    context = {
        "category": category
    }
    return render(request, "index.html", context)


def product(request):
    product = Products.objects.all().order_by("id")
    mygoods = Paginator(product, 4)
    next_page_prod = request.GET.get("page")
    mygoods_good = mygoods.get_page(next_page_prod)
    context = {
        "mygoods_good": mygoods_good,
    }
    return render(request, "product.html", context)


def product_category(request, slug):
    prod_cat = Products.objects.filter(category__slug=slug).all()
    context = {
        "product_category": prod_cat,
    }
    return render(request, "category.html", context)

def categories(request):
    categories = Category.objects.all().order_by("id")
    context = {
        "categories": categories,
    }
    return render(request, "categories.html", context)

def details(request, id):
    details = get_object_or_404(Products, id=id)
    context = {
        "details": details,
    }
    return render(request, "details.html", context)

def contact(request):
    form = ContactForm()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for contacting us!...")
            return redirect("index")
        else:
            messages.error(request, form.errors)
            return redirect("index")
    return redirect("index")

def signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"welcome {username}! FlickBusters, we hope you have the best experience with us.....")
            return redirect("index")
        else:
            messages.error(request, "Invalid username or password. Please confirm again.")
            return redirect("signin")
    return render(request, "signin.html")

def signup(request):
    form = SignupForm()
    if request.method == "POST":
        phone = request.POST["phone"]
        profile_img = request.POST["profile_img"]
        form = SignupForm(request.POST)
        if form.is_valid():
            newuser = form.save()
            newprofile= Profile(user=newuser)
            newprofile.user = newuser
            newprofile.first_name = newuser.first_name
            newprofile.last_name = newuser.last_name
            newprofile.email = newuser.email
            newprofile.phone = phone
            newprofile.profile_img = profile_img
            newprofile.save()
            messages.success(request, f"Welcome to Flickbusters {newuser}")
            return redirect("index")
        else:
            messages.error(request, form.errors)
            return redirect("signup")
    return render(request, "signup.html")

@login_required(login_url="signin")
def profile(request):
    user_profile = Profile.objects.get(user__username=request.user.username)
    context = {
        "profile": user_profile,
    }
    return render(request, "profile.html", context)

@login_required(login_url="signin")
def profile_update(request):
    profile = Profile.objects.get(user__username=request.user.username)
    update = ProfileUpdate(instance=request.user.profile)
    if request.method == "POST":
        update = ProfileUpdate(request.POST, request.FILES, instance=request.user.profile)
        if update.is_valid():
            update.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect("profile")
        else:
            messages.error(request, update.errors)
            return redirect("profile")
    # context = {
    #     "profile": profile,
    #     "update": update,
    # }
    return redirect("profile")

@login_required(login_url="signin")
def password(request):
    profile = Profile.objects.get(user__username = request.user.username)
    form = PasswordChangeForm(request.user)
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password Changed Successfully!..")
            return redirect("profile")
        else:
            messages.error(request, form.errors)
            return redirect("password")
    context = {
        "form": form,
        "profile": profile,
    }
    return render(request, "password.html", context)


@login_required(login_url="signin")
def signout(request):
    logout(request)
    return redirect("signin")

def search(request):
    if request.method == "POST":
        items = request.POST["search"]
        searched_items = Q(Q(title__icontains =items) | Q(category__name__icontains=items))
        searched_goods = Products.objects.filter(searched_items)
        context = {
            "items": items,
            "searched_goods":searched_goods,
        }
        
        return render(request, "search.html", context)
    else:
        return render(request, "search.html")

@login_required(login_url="signin")
def shopcart(request):
    if request.method == "POST":
        quantity = int(request.POST["quantity"])
        item_id = request.POST["product_id"]
        product = Products.objects.get(pk=item_id)
        order_num = Profile.objects.get(user__username= request.user.username)
        cart_no = order_num.id 

        cart = Shopcart.objects.filter(user__username=request.user.username)
        if cart:
            basket = Shopcart.objects.filter(product_id=product.id, user__username= request.user.username, paid=False).first()
            if basket:
                basket.quantity += quantity
                basket.amount = basket.price * basket.quantity 
                basket.save()
                messages.success(request, f"{product.title} has been added to cart successfully!..")
                return redirect("product")
            else:
                cartitems = Shopcart()
                cartitems.user = request.user
                cartitems.product = product 
                cartitems.title = product.title
                cartitems.quantity = quantity
                cartitems.amount = product.price * quantity
                cartitems.price = product.price
                cartitems.paid = False
                cartitems.order_no = cart_no
                cartitems.save()
                messages.success(request, f"{product.title} has been added to cart successfully!...")
                return redirect("product")
        else:
            cartprod = Shopcart()
            cartprod.user = request.user
            cartprod.product = product 
            cartprod.title = product.title
            cartprod.quantity = quantity
            cartprod.amount = product.price * quantity
            cartprod.price = product.price
            cartprod.paid = False
            cartprod.order_no = cart_no
            cartprod.save()
            messages.success(request, f"{product.title} has been added to cart successfully!...")
            return redirect("product")
    return redirect("shopcart")

@login_required(login_url="signin")
def displaycart(request):
    basket = Shopcart.objects.filter(user__username=request.user.username, paid=False)
    subtotal = 0
    vat = 0
    total = 0

    for cart in basket:
        subtotal += cart.price * cart.quantity

    vat = 0.075 * subtotal 
    total = subtotal + vat 

    
    context = {
        "basket": basket,
        "total": total,
        "vat": vat,
        "subtotal": subtotal,
    }
    return render(request, "shopcart.html", context)

@login_required(login_url="signin")
def deleteitems(request):
    try:
        if request.method == "POST":
            items = request.POST["items_id"]
            deletecart = Shopcart.objects.get(pk=items)
            deletecart.delete()
            messages.success(request, f"{deletecart.title} has been deleted successfully...")
            return redirect("displaycart")
    except Shopcart.DoesNotExist:
        messages.error(request, f"{deletecart.title} does not exist")
        return redirect("displaycart")
    
@login_required(login_url="signin")
def modifycart(request):
    try:
        if request.method == "POST":
            quantity = int(request.POST["quantity"])
            items = request.POST["product_id"]
            modify = Shopcart.objects.get(pk=items)
            modify.quantity += quantity
            modify.amount = modify.price * modify.quantity
            modify.save()
            messages.success(request, f"{modify.title} has been updated successfully!..")
            return redirect("displaycart")
    except Shopcart.DoesNotExist:
        messages.error(request, f"{modify.title} does not exist")
        return redirect("displaycart")


@login_required(login_url="signin")
def checkout(request):
    profile = Profile.objects.get(user__username=request.user.username)
    basket = Shopcart.objects.filter(user__username=request.user.username, paid=False)
    subtotal = 0
    vat = 0
    total = 0

    for cart in basket:
        subtotal += cart.price * cart.quantity

    vat = 0.075 * subtotal 
    total = subtotal + vat 

    
    context = {
        "basket": basket,
        "total": total,
        "vat": vat,
        "subtotal": subtotal,
        "profile": profile,
    }
    return render (request, "checkout.html", context)

# sk_test_43762140e809dbc5ffee4d9c1e84d8c72afd6b9d
@login_required(login_url="signin")
def pay(request):
    if request.method == "POST":
        api_key = "sk_test_43762140e809dbc5ffee4d9c1e84d8c72afd6b9d"
        curl = "https://api.paystack.co/transaction/initialize"
        cburl = "http://127.0.0.1:8990/callback/"
        ref = str(uuid.uuid4())
        profile = Profile.objects.get(user__username= request.user.username)
        shop_code = profile.id
        user = User.objects.get(username=request.user.username)
        first_name = profile.first_name
        last_name = profile.last_name
        email = profile.email
        total = float(request.POST["total"]) * 100
        phone = request.POST["phone"]
        address = request.POST["address"]
        headers = {"Authorization": f"Bearer {api_key}"}
        data = {"reference": ref,  "callback_url": cburl, "order_number": shop_code,
                 "amount": int(total), "email":email, "currency": "NGN"}
        
        try:
            r = requests.post(curl, headers=headers, data=data)
        except Exception:
            messages.error(request, "Network Busy, Try again Later...")
        else:
            transback = json.loads(r.text)
            rdurl = transback["data"]["authorization_url"]

            account = Payment()
            account.user = user 
            account.first_name = first_name
            account.last_name = last_name
            account.email = email
            account.phone = phone
            account.address = address
            account.pay_code = ref 
            account.shop_code = shop_code
            account.paid = True
            account.amount = total / 100
            account.save()
        return redirect(rdurl)
    return redirect("checkout")

@login_required(login_url="signin")
def callback(request):
    profile = Profile.objects.filter(user__username=request.user.username)
    basket = Shopcart.objects.filter(user__username=request.user.username, paid=False)
    paid = Payment.objects.filter(user__username=request.user.username, paid=True)

    for items in basket:
        items.paid = True 
        items.save()

        stock = Products.objects.get(pk = items.product_id)
        stock.max_quantity -= items.quantity
        stock.save()
    context = {
        "profile": profile,
        "paid": paid,
    }
    return render(request, "callback.html", context)