from django.contrib import admin

from MarketplaceProject.web.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']