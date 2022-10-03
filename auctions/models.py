from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"


class Category(models.Model):
    category = models.CharField(max_length=64)
    def __str__(self):
        return f"{self.category}"


class Listing(models.Model):
    title = models.CharField(max_length=64)
    listing_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    start_bid = models.DecimalField(max_digits=5, decimal_places=2)
    highest_bid = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    description = models.TextField()
    picture = models.URLField(blank=True)
    active = models.BooleanField(default=True)
    publication_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.id}" 


class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user_bid = models.DecimalField(max_digits=5, decimal_places=2)
    is_winner = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.id}"


class Comment(models.Model):
    user_comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    comment_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user}"