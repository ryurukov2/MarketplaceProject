from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy

from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from MarketplaceProject.auth_app.models import Profile
from django.views.generic import DetailView

from MarketplaceProject.web.forms import ListingForm, ListingWithImagesForm, ProductImageFormset
from MarketplaceProject.web.models import Listing

UserModel = get_user_model()

# Create listing view
class ListingImageUploadView(CreateView):
    model = Listing
    form_class = ListingWithImagesForm
    template_name = 'web_app/listing_form.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['product_images'] = ProductImageFormset(self.request.POST, self.request.FILES)
        else:
            data['product_images'] = ProductImageFormset()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        form.instance.seller = Profile.objects.get(user_id=self.request.user.id)
        product_images = context['product_images']
        self.object = form.save()
        if product_images.is_valid():
            product_images.instance = self.object
            product_images.save()
        return super().form_valid(form)


# class ListingEditView(UpdateView):
#     model = Listing
#     # fields = ['first_name', 'last_name', 'age', 'city', 'bio', 'profile_picture', ]
#     form_class = ListingWithImagesForm
#     template_name = 'web_app/edit_listing.html'
#
#     def __init__(self):
#         super().__init__()
#         self.object = None
#
#     def get(self, request, *args, **kwargs):
#         self.object = self.get_object()
#
#         # Check if the logged-in user is the owner of the profile that is being edited
#         if self.object.seller.user != request.user:
#             return redirect('listing detail', pk=self.object.id)
#
#         context = self.get_context_data(object=self.object)
#         return self.render_to_response(context)

# LoginRequiredMixin

# def addNoteView(request):
#     if request.method == "POST":
#         # images will be in request.FILES
#         form = FullListingForm(request.POST or None, request.FILES or None)
#         files = request.FILES.getlist('product_photos')
#         if form.is_valid():
#             user = request.user
#             title = form.cleaned_data['title']
#             price = form.cleaned_data['price']
#             description = form.cleaned_data['description']
#             category = form.cleaned_data['category']
#             listing_obj = Listing.objects.create(seller=user,
#                                                  title=title,
#                                                  description=description,
#                                                  category=category,
#                                                  price=price
#                                                  )
#             for f in files:
#                 ProductImage.objects.create(listing=listing_obj, image=f)
#         else:
#             print("Form invalid")

# working well for one image per listing, but not sufficient
# class ListingCreateView(LoginRequiredMixin, CreateView):
#     model = Listing
#     # fields = ['title', 'price', 'description', 'category', 'product_photos',]
#     template_name = 'web_app/listing_form.html'
#     form_class = ListingForm
#
#     # success_url =

#     def form_valid(self, form):
#         # Set the seller field to the currently logged in user (Profile)
#         form.instance.seller = Profile.objects.get(user_id=self.request.user.id)
#         return super().form_valid(form)

# def form_valid(self, form):
#     form.instance.seller = Profile.objects.get(user_id=self.request.user.id)
#     # Save the form data to the database
#     response = super().form_valid(form)
#     # Get the primary key of the newly created listing
#     listing_pk = self.object.pk
#     # Use the reverse function to generate the URL for the listing detail view
#     listing_detail_url = reverse('listing detail', kwargs={'pk': listing_pk})
#     # Return a redirect response to the listing detail URL
#     return redirect(listing_detail_url)


class ListingDetailView(DetailView):
    model = Listing
    template_name = 'web_app/listing_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        listing = context['listing']
        images = listing.productimage_set.all()
        context['images'] = images
        return context


# class EditListingView(View):
#     def get(self, request, pk):
#         listing = get_object_or_404(Listing, pk=pk)
#         form = ListingForm(instance=listing)
#         return render(request, 'web_app/edit_listing.html', {'form': form, 'listing': listing})
#
#     def post(self, request, pk):
#         listing = get_object_or_404(Listing, pk=pk)
#         form = ListingForm(request.POST, instance=listing)
#         if form.is_valid():
#             listing = form.save()
#             return redirect(listing.get_absolute_url())
#         return render(request, 'web_app/edit_listing.html', {'form': form, 'listing': listing})




class ListingImageUpdateView(UpdateView):
    model = Listing
    form_class = ListingWithImagesForm
    template_name = 'web_app/edit_listing.html'
    MAXIMUM_IMAGES = 5

    def __init__(self):
        super().__init__()
        self.object = None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Check if the logged-in user is the owner of the profile that is being edited
        if self.object.seller.user != request.user:
            return redirect('listing detail', pk=self.object.id)

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['product_images'] = ProductImageFormset(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['product_images'] = ProductImageFormset(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        product_images = context['product_images']
        self.object = form.save()
        if product_images.is_valid():
            product_images.instance = self.object
            product_images.save()
        return super().form_valid(form)


class ListingListView(ListView):
    model = Listing
    template_name = 'index.html'


class ListingDeleteView(DeleteView):
    model = Listing
    success_url = reverse_lazy('index')



