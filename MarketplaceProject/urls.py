from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth_app/', include('MarketplaceProject.auth_app.urls')),
    path('', include('MarketplaceProject.web.urls')),
]
