from django.contrib import admin
from django.contrib.auth import admin as auth_admin, get_user_model

from MarketplaceProject.auth_app.forms import SignUpForm, AppUserCreationForm, ProfileUpdateForm, AppUserViewForm
from MarketplaceProject.auth_app.models import AppUser, Profile

UserModel = get_user_model()


# @admin.register(UserModel)
# class AppUserAdmin(auth_admin.UserAdmin):
#     USERNAME_FIELD = 'email'
#
#     def save_model(self, request, obj, form, change):
#         obj.save()
#         form.save(commit=True)
#
#     ordering = ('email',)
#     list_display = ['email', 'date_joined', 'last_login', 'is_staff']
#     list_filter = ()
#     add_form = SignUpForm
#     exclude = ('date_joined', 'username', 'is_active', 'first_name', 'last_name')
#     add_fieldsets = (
#         (
#             None,
#             {
#                 "classes": ("wide",),
#                 "fields": ("email", "password1", "password2"),
#             },
#         ),
#         (
#             None,
#             {
#                 "classes": ("wide",),
#                 "fields": ("first_name", "last_name", "age", "city", "is_staff", "bio",),
#             },
#         ),
#     )

# class AppUserAdmin(admin.ModelAdmin):
#     form = AppUserForm
#
#
# admin.site.register(AppUser, AppUserAdmin)


class ProfileInline(admin.TabularInline):
    model = Profile
    form = ProfileUpdateForm
    can_delete = False


class AppUserAdmin(admin.ModelAdmin):
    model = AppUser
    form = AppUserCreationForm
    list_display = ['email', 'is_staff']
    readonly_fields = ('is_superuser',)
    exclude = ('password',)
    inlines = [
        ProfileInline,
    ]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields
        return ()

    def add_view(self, request, form_url="", extra_context=None):
        self.exclude = ('last_login', 'password', 'is_superuser')
        return super(AppUserAdmin, self).add_view(request)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        # self.exclude = ('last_login', 'password', 'password1', 'password2')
        self.fields = ('email', 'is_staff', 'groups', 'is_superuser',)
        self.form = AppUserViewForm
        return super(AppUserAdmin, self).change_view(request, object_id)


class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ['user', 'first_name', 'last_name', 'age', 'city']


#
admin.site.register(AppUser, AppUserAdmin)
admin.site.register(Profile, ProfileAdmin)
