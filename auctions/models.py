from decimal import Decimal

from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator

from account.models import User


class Category(models.Model):
    """A category model."""

    name = models.CharField(max_length=80)
    slug = models.SlugField(max_length=80, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('auctions:listings', args=[self.slug])

class Listing(models.Model):
    """A listing model."""

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField()
    start_bid = models.DecimalField(max_digits=9, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))])
    image = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('auctions:listing', kwargs={
            'cat_slug': self.category.slug, 'listing_slug': self.slug
        })

class Bid(models.Model):
    """A bid model."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bid = models.DecimalField(max_digits=19, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    """A comment model."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    text = models.TextField(max_length=3000)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    # is_active = models.BooleanField(default=False)

class Watchlist(models.Model):
    """A watchlist model."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
