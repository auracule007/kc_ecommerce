from django.contrib import admin
from django.contrib.admin import ModelAdmin
from . models import *

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "slug", "img", "description", "date_added"]
admin.site.register(Category, CategoryAdmin)

class ProductsAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "category", "slug", "price", "description", "img",
      "quantity", "max_quantity", "min_quantity", "date_added"]
admin.site.register(Products, ProductsAdmin)

class ContactAdmin(admin.ModelAdmin):
    list_display = ["id", 'full_name', "email", "subject", "message", "date_added"]
admin.site.register(Contact, ContactAdmin)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ["id","first_name", "last_name", "email", "phone", "profile_img"]
admin.site.register(Profile, ProfileAdmin)


admin.site.register(Shopcart)
admin.site.register(Payment)