from django.contrib.auth import views as auth_views, login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as views
from django.views.generic import UpdateView, DetailView

from MarketplaceProject.auth_app.forms import SignUpForm, ProfileUpdateForm
from MarketplaceProject.auth_app.models import Profile


class SignUpView(views.CreateView):
    template_name = 'auth_app/sign-up.html'
    form_class = SignUpForm

    success_url = reverse_lazy('index')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['form'] = SignUpForm()
    #     return context
    def form_valid(self, form):
        result = super().form_valid(form)

        login(self.request, self.object)
        return result


class SignInView(auth_views.LoginView):
    template_name = 'auth_app/login.html'
    success_url = reverse_lazy('index')

    def get_success_url(self):
        if self.success_url:
            return self.success_url

        return self.get_redirect_url() or self.get_default_redirect_url()


class SignOutView(auth_views.LogoutView):
    template_name = 'auth_app/sign-out.html'

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
            return redirect('profile detail', pk=self.object.user_id)

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


