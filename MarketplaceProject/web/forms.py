from django import forms
from MarketplaceProject.web.models import Listing


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'price', 'description', 'category']
