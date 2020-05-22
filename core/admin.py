from django.contrib import admin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
import django.forms as forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from hijack_admin.admin import HijackUserAdminMixin

from core.models import Message, User, SystemVariable

admin.site.register(Message)
admin.site.register(SystemVariable)

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = '__all__'

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
        """A form for updating users. Includes all the fields on
        the user, but replaces the password field with admin's
        password hash display field.
        """
        password = ReadOnlyPasswordHashField()

        class Meta:
            model = User
            fields = '__all__'

        def clean_password(self):
            # Regardless of what the user provides, return the initial value.
            # This is done here, rather than on the field, because the
            # field does not have access to the initial value
            return self.initial["password"]


class UserAdmin(BaseUserAdmin, HijackUserAdminMixin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_officer', 'is_technician', 'hijack_field',
                    'last_login')
    list_filter = ('is_officer',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'last_password_update')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'order_in_app', 'last_login', 'phone')}),
        ('Tokens', {'fields': ('pb_token', 'telegram_token')}),
        ('Permissions', {'fields': ('is_active', 'is_officer', 'is_technician', 'is_google')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'pb_token', 'order_in_app', 'is_officer', 'is_technician',
                       'is_google', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
