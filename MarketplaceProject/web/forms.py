from django import forms
from MarketplaceProject.auth_app.models import Profile


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'age', 'city', 'bio', 'profile_picture']