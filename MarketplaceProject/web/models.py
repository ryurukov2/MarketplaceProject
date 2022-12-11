from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db import models

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

