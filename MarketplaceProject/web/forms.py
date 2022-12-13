from django import forms
from django.forms import ClearableFileInput

from MarketplaceProject.web.models import Listing, ProductImage


class ListingForm1(forms.ModelForm):
    product_photos = forms.ImageField(widget=ClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta:
        model = Listing
        fields = ['title', 'price', 'description', 'category', 'product_photos']

    def save(self, commit=True):
        listing = super().save(commit=commit)
        image = ProductImage(
            product_photos=self.cleaned_data['product_photos'],
            listing=listing
        )
        if commit:
            image.save()

        return listing

        # for image_file in self.cleaned_data['product_photos']:
        #     image = ProductImage(
        #         product_photos=image_file,
        #         listing=listing
        #     )
        #     if commit:
        #         image.save()


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'price', 'description', 'category']


ProductImageFormset = forms.inlineformset_factory(Listing, ProductImage, fields=('product_photos',), extra=3)


class ListingWithImagesForm(ListingForm):
    product_images = ProductImageFormset()

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.product_image_formset = forms.inlineformset_factory(Listing, ProductImage, fields=('product_photos',))
    #
    #     if self.instance is None:
    #         # Form is being used to create a new listing
    #         self.product_images.set_extra(3)
    #     else:
    #         # Form is being used to update an existing listing
    #         self.product_images.set_extra(2)
