from django.db import models
from django.contrib.auth.models import User

class UserLogin(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.user.username} - {self.login_time}"

# Category for organizing products
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

# Product Model
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    rating = models.FloatField(default=0) # 0 to 5
    is_new = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    category = models.CharField(max_length=50)
    type  = models.CharField(max_length=50)
    discription = models.CharField(max_length=500)


##Men Fasion 

class MenProduct(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='men_products/')
    is_featured = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    rating = models.FloatField(default=0)

    def __str__(self):
        return self.name    
 



# Cart Item 
class cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    session_key = models.CharField(max_length=100)  # for guest users

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    



class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # ✅ for logged-in users
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    session_key = models.CharField(max_length=100, null=True, blank=True)  # ✅ still support guest carts

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"    

# Order (optional)
class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return f"Order #{self.id}"
    

##contact Us 
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"    
    

##UserProfile....

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    image=models.ImageField(upload_to='User/profile')
    City = models.TextField(blank=True)



    def __str__(self):
        return self.user.username

##Profile 

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    age = models.IntegerField(null=True, blank=True)
    image = models.ImageField(upload_to='profiles/', default='profiles/default.png')
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    city = models.CharField(max_length=100)
    region_state = models.CharField(max_length=50, null=True, blank=True)
    district = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username
    




class Transaction(models.Model):
    PAYMENT_GATEWAYS = [
        ('esewa', 'eSewa'),
        ('khalti', 'Khalti'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gateway = models.CharField(max_length=20, choices=PAYMENT_GATEWAYS)
    order_id = models.CharField(max_length=100)
    amount = models.PositiveIntegerField()
    token = models.CharField(max_length=255, null=True, blank=True)  # for Khalti
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.gateway.upper()} | {self.order_id} | {self.status}"




