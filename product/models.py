from django.db import models
import uuid
from django.contrib.auth.models import User
# Create your models here.
class ProductType(models.Model):
    name=models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    product_type=models.ForeignKey(ProductType, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    price=models.IntegerField()
    description=models.TextField()
    image=models.ImageField(upload_to='product_image', blank=True)
    
    def __str__(self):
        return self.name

class Cart(models.Model):
    id=models.UUIDField(default=uuid.uuid4, primary_key=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    completed=models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.id)

class CartItem(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
    cart=models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartitems')
    quantity=models.IntegerField(default=0)
    
    def __str__(self):
        return self.product.name
    
class Order(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    cart=models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity=models.IntegerField()
    total_amount=models.DecimalField(max_digits=6, decimal_places=2)
    timestamp=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username

class OrderUserInfo(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    order=models.ForeignKey(Order, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    
    def __str__(self):
        return self.name