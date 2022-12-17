from django.contrib import admin

from MarketplaceProject.web.models import Category, Listing, ProductImage


class ProductImagesInline(admin.TabularInline):
    model = ProductImage
    can_delete = False

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'category', 'seller']
    inlines = [
        ProductImagesInline,
    ]
