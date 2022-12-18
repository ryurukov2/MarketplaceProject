from django.contrib.auth import forms as auth_forms, get_user_model
from django import forms
from MarketplaceProject.auth_app.models import Profile, AppUser

UserModel = get_user_model()


class AppUserViewForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = '__all__'
        exclude = ('password',)
        field_classes = {'email': forms.EmailField}


class AppUserCreationForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = '__all__'
        exclude = ('password',)
        field_classes = {'email': forms.EmailField}

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class SignUpForm(auth_forms.UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    age = forms.IntegerField()
    city = forms.CharField(required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    profile_picture = forms.ImageField(required=False)

    # @Babayaga123
    class Meta:
        model = UserModel
        fields = (UserModel.USERNAME_FIELD, 'password1', 'password2', 'first_name',
                  'last_name', 'age', 'city', 'bio', 'profile_picture',)
        USERNAME_FIELD = 'email'

    # save with data for profile
    def save(self, commit=True):
        user = super().save(commit=commit)
        print('from save')
        profile = Profile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            age=self.cleaned_data['age'],
            bio=self.cleaned_data['bio'],
            city=self.cleaned_data['city'],
            profile_picture=self.cleaned_data['profile_picture'],
            user=user,
        )
        if commit:
            profile.save()

        return user


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'age', 'city', 'bio', 'profile_picture']
