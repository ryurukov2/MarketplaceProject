from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404

from django.views import View
from django.views.generic import ListView, UpdateView, CreateView
from MarketplaceProject.auth_app.models import Profile
from django.views.generic import DetailView

from MarketplaceProject.web.forms import ListingForm
from MarketplaceProject.web.models import Listing

UserModel = get_user_model()


# LoginRequiredMixin
class UsersListView(ListView):
    model = UserModel
    template_name = 'index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        print(self.request.user.__class__)
        return context


# LoginRequiredMixin,



class ListingCreateView(LoginRequiredMixin, CreateView):
    model = Listing
    fields = ['title', 'price', 'description', 'category']
    template_name = 'web_app/listing_form.html'

    # success_url =
    def form_valid(self, form):
        # Set the seller field to the currently logged in user (Profile)
        form.instance.seller = Profile.objects.get(user_id=self.request.user.id)
        return super().form_valid(form)

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

class EditListingView(UpdateView):
    model = Listing
    # fields = ['first_name', 'last_name', 'age', 'city', 'bio', 'profile_picture', ]
    form_class = ListingForm
    template_name = 'web_app/edit_listing.html'

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