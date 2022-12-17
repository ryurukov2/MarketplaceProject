from django.db import models

from django.contrib.auth import models as auth_models
from django.db import models
from django.urls import reverse
from django.utils import timezone

from MarketplaceProject.auth_app.managers import AppUserManager


class AppUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
    )
    is_staff = models.BooleanField(
        default=False,
        null=False,
        blank=False,
    )

    USERNAME_FIELD = 'email'

    objects = AppUserManager()


class Profile(models.Model):
    first_name = models.CharField(
        max_length=25
    )
    last_name = models.CharField(
        max_length=25
    )
    age = models.PositiveIntegerField()

    user = models.OneToOneField(
        AppUser,
        primary_key=True,
        on_delete=models.CASCADE,
    )

    city = models.CharField(max_length=255, blank=True, null=True)

    bio = models.TextField(blank=True, null=True)

    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    def get_absolute_url(self):
        return reverse('profile detail', kwargs={'pk': self.pk})
