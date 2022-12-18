from django import forms
from django.forms import ClearableFileInput

from MarketplaceProject.web.models import Listing, ProductImage


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'price', 'description', 'category']


ProductImageFormset = forms.inlineformset_factory(Listing, ProductImage, fields=('product_photos',), extra=3)


class ListingWithImagesForm(ListingForm):
    product_images = ProductImageFormset()


