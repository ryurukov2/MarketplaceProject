from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.utils import timezone

from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from MarketplaceProject.auth_app.models import Profile
from django.views.generic import DetailView

from MarketplaceProject.web.forms import ListingForm, ListingWithImagesForm, ProductImageFormset
from MarketplaceProject.web.models import Listing, Message, Thread

UserModel = get_user_model()


# Create listing view
class ListingImageUploadView(LoginRequiredMixin, CreateView):
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





class ListingDetailView(DetailView):
    model = Listing
    template_name = 'web_app/listing_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['user'] = self.request.user
        listing = context['listing']
        images = listing.productimage_set.all()
        context['images'] = images
        return context




class ListingImageUpdateView(UpdateView):
    model = Listing
    form_class = ListingWithImagesForm
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


class ListingDeleteView(LoginRequiredMixin, DeleteView):
    model = Listing
    success_url = reverse_lazy('index')

    ########


def send_message(request, pk):
    sender_id = request.user.id
    message_body = request.POST.get('message_body')
    timestamp = timezone.now()

    try:
        sender = Profile.objects.get(pk=sender_id)
        recipient = Profile.objects.get(pk=pk)
    except Profile.DoesNotExist:
        return HttpResponse('Profile matching query does not exist.')
    thread, created = Thread.objects.get_or_create(sender, recipient)
    message = Message(
        sender=sender,
        recipient=recipient,
        message_body=message_body,
        timestamp=timestamp,
        thread=thread
    )
    message.save()

    return redirect('view_messages', pk=recipient.pk)


@login_required
def message_form(request, pk):
    try:
        Profile.objects.get(pk=pk)
    except Profile.DoesNotExist:
        return redirect('index')
    if request.user.id == pk:
        return redirect('profile detail', pk=pk)
    return render(request, 'web_app/message_form.html', context={'pk': pk})


#
@login_required
def view_threads(request):
    profile = Profile.objects.get(user_id=request.user.id)
    threads = list(Thread.objects.filter(user_1=profile) | Thread.objects.filter(user_2=profile))
    _ = 0
    for i in range(len(threads)):
        if not Message.objects.filter(thread=threads[_].id):
            threads[_].delete()
            threads.pop(_)
            _ -= 1

        _ += 1
    return render(request, 'web_app/view_threads.html', {'threads': threads})


@login_required
def view_thread_messages(request, pk):
    try:
        Profile.objects.get(pk=pk)
    except Profile.DoesNotExist:
        return redirect('view_threads')
    # if request.user.id == pk:
    #     return redirect('profile detail', pk=pk)
    sender = Profile.objects.get(user_id=request.user.id)
    recipient = Profile.objects.get(user_id=pk)
    thread, created = Thread.objects.get_or_create(sender, recipient)
    if thread.user_1_id == request.user.id:
        receiver_id = thread.user_2_id
    else:
        receiver_id = thread.user_1_id
    return render(request, 'web_app/view_messages.html', {'thread': thread,
                                                          'pk': receiver_id})


def listings_search(request):
    query = request.GET.get('q')
    listings = None
    if query:
        listings = Listing.objects.all().filter(title__icontains=query) | Listing.objects.all().filter(
            description__icontains=query)

    return render(request, 'web_app/search_results.html', {'listings': listings})
