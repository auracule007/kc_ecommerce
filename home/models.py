from django.db import models
from  django.contrib.auth.models import User 
import uuid 

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(default="")
    img = models.ImageField(default="category.jpg", upload_to="Category")
    description = models.TextField()
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name 
    
class Products(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    slug = models.SlugField(default="")
    price = models.IntegerField()
    description = models.TextField()
    img = models.FileField(upload_to="Product", default="product.jpg")
    quantity = models.IntegerField()
    max_quantity = models.IntegerField()
    min_quantity = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} --- {self.category.name}"
    
class Contact(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    profile_img = models.FileField(upload_to="Profile", default="profile.jpg")
    
    def __str__(self):
        return self.user.username
    
class Shopcart(models.Model):
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    price = models.IntegerField()
    amount = models.IntegerField()
    quantity = models.IntegerField()
    order_no = models.CharField(max_length=50, default="")
    paid = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.title 
    

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    amount = models.CharField(max_length=100, default="")
    phone = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    paid = models.BooleanField(default=False)
    pay_code = models.CharField(max_length=50)
    shop_code = models.CharField(max_length=50)
    pay_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
