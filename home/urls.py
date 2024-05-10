from django.urls import path 
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("product/", views.product, name="product"),
    path("product/<slug:slug>/", views.product_category, name="product_category"),
    path("categories/", views.categories, name="categories"),
    path("details/<str:id>/", views.details, name="details"),
    path("contact/", views.contact, name = "contact"),

    path("signin/", views.signin, name="signin"),
    path("signup/", views.signup, name="signup"),
    path("profile/", views.profile, name="profile"),
    path("profile_update/", views.profile_update, name="profile_update"),
    path("password/", views.password, name="password"),
    path("signout/", views.signout, name="signout"),
    path("search/", views.search, name="search"),

    path("shopcart/", views.shopcart, name="shopcart"),
    path("displaycart/", views.displaycart, name="displaycart"),
    path("deleteitems/", views.deleteitems, name="deleteitems"),
    path("modifycart/", views.modifycart, name="modifycart"),
    path("checkout/", views.checkout, name="checkout"),
    path("pay/", views.pay, name="pay"),
    path("callback/", views.callback, name="callback"),
]