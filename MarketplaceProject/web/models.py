from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone

from MarketplaceProject.auth_app.models import Profile
from MarketplaceProject.web.managers import ThreadManager

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

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('listing detail', kwargs={'pk': self.pk})


class ProductImage(models.Model):
    class Meta:
        ordering = ['id']
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    product_photos = models.ImageField(upload_to='product_photos/')


class Thread(models.Model):
    objects = ThreadManager()
    user_1 = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='user_1_threads'
    )
    user_2 = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='user_2_threads'
    )
    timestamp = models.DateTimeField(auto_now=True)


class Message(models.Model):
    class Meta:
        ordering = ['timestamp']

    sender = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    recipient = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    message_body = models.TextField(blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    thread = models.ForeignKey(
        Thread,
        on_delete=models.CASCADE,
        related_name='messages',
        blank=False,
        null=False
    )
