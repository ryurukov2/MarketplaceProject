from django.urls import path

from MarketplaceProject.web.views import UsersListView, ProfileDetailView, ProfileUpdateView

urlpatterns = [
    path('', UsersListView.as_view(), name='index'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile detail'),
    path('profile_edit/<int:pk>/', ProfileUpdateView.as_view(), name='profile_edit'),
]