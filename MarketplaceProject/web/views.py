from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView, UpdateView
from MarketplaceProject.auth_app.models import Profile
from django.views.generic import DetailView

from MarketplaceProject.web.forms import ProfileUpdateForm

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
class ProfileDetailView(DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = 'web_app/profile_detail.html'

    def __init__(self):
        super().__init__()
        self.object = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['app_user'] = self.object.user
        context['user'] = self.request.user
        return context

    # moved logic to template
    # def get(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     if self.object.user != request.user:
    #         return redirect('index')
    #
    #     context = self.get_context_data(object=self.object)
    #     return self.render_to_response(context)


class ProfileUpdateView(UpdateView):
    model = Profile
    # fields = ['first_name', 'last_name', 'age', 'city', 'bio', 'profile_picture', ]
    form_class = ProfileUpdateForm
    template_name = 'web_app/profile_form.html'

    def __init__(self):
        super().__init__()
        self.object = None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Check if the logged-in user is the owner of the profile that is being edited
        if self.object.user != request.user:
            return redirect('index')

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
