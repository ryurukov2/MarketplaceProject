from django.urls import path

from MarketplaceProject.auth_app.views import ProfileDetailView, ProfileUpdateView
from MarketplaceProject.web.views import UsersListView, ListingCreateView, \
    ListingDetailView, EditListingView

urlpatterns = [
    path('', UsersListView.as_view(), name='index'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile detail'),
    path('profile_edit/<int:pk>/', ProfileUpdateView.as_view(), name='profile_edit'),
    path('listing_new/', ListingCreateView.as_view(), name='listing new'),
    path('listing/<int:pk>/', ListingDetailView.as_view(), name='listing detail'),
    path('listing_edit/<int:pk>/', EditListingView.as_view(), name='listing edit'),
]
