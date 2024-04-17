from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse 
import datetime

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.user.username


class Item(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="uploads/%Y/%m/%d/" , null= True , blank=True) 
    price = models.DecimalField(max_digits=10, decimal_places=2)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    is_sold = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)


    def get_absolute_url(self):
        """Returns the url to access a particular genre instance."""
        return reverse('item-detail', args=[str(self.id)])
    
    def __str__(self):
        return self.title
    

class Transaction(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart item {self.item} for user {self.user}"