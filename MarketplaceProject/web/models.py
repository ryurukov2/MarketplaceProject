from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone

from MarketplaceProject.auth_app.models import Profile

GeneralUser = get_user_model()


class Category(models.Model):
    class Meta:
        verbose_name_plural = "categories"

    name = models.CharField(
        max_length=50,
        null=False,
        blank=False,
    )
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Listing(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default='General')
    seller = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('listing detail', kwargs={'pk': self.pk})


class ProductImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    product_photos = models.ImageField(upload_to='product_photos/')
