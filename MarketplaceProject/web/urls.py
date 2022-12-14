from django.urls import path

from MarketplaceProject.auth_app.views import ProfileDetailView, ProfileUpdateView
from MarketplaceProject.web.views import ListingListView, \
    ListingDetailView, ListingDeleteView, ListingImageUploadView, ListingImageUpdateView

urlpatterns = [
    path('', ListingListView.as_view(), name='index'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile detail'),
    path('profile_edit/<int:pk>/', ProfileUpdateView.as_view(), name='profile_edit'),
    path('listing_new/', ListingImageUploadView.as_view(), name='listing new'),
    path('listing/<int:pk>/', ListingDetailView.as_view(), name='listing detail'),
    path('listing_edit/<int:pk>/', ListingImageUpdateView.as_view(), name='listing edit'),
    path('listing_remove/<int:pk>/', ListingDeleteView.as_view(), name='listing delete'),
]
