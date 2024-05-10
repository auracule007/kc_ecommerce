from . models import *


def cartcount(request):
    reading = Shopcart.objects.filter(user__username=request.user.username, paid=False)
    cartcount = 0

    for items in reading:
        cartcount += items.quantity
    context = {
        "cartcount": cartcount,
    }
    return context 


def category(request):
    category = Category.objects.all().order_by("id")
    context = {
        "category":category,
    }
    return context 