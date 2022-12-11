from django.contrib.auth import forms as auth_forms, get_user_model
from django import forms
from MarketplaceProject.auth_app.models import Profile

UserModel = get_user_model()


class SignUpForm(auth_forms.UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    age = forms.IntegerField()
    city = forms.CharField(required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = UserModel
        fields = (UserModel.USERNAME_FIELD, 'password1', 'password2', 'first_name',
                  'last_name', 'age', 'city', 'bio',)

    # save with data for profile
    def save(self, commit=True):
        user = super().save(commit=commit)

        profile = Profile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            age=self.cleaned_data['age'],
            bio=self.cleaned_data['bio'],
            city=self.cleaned_data['city'],
            user=user,
        )
        if commit:
            profile.save()

        return user
