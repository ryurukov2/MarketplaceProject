from django.urls import path

from MarketplaceProject.auth_app.views import SignUpView, SignInView, SignOutView

urlpatterns = [
    path('sign-up/', SignUpView.as_view(), name='sign up'),
    path('sign-in/', SignInView.as_view(), name='login'),
    path('sign-out/', SignOutView.as_view(), name='sign out'),
]
