from django import forms
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm, PasswordChangeForm


class MundiaguaLoginForm(AuthenticationForm):
    password = forms.CharField(label="Password", strip=False,
                               widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))


class MundiaguaChangePasswordForm(PasswordChangeForm, SetPasswordForm):

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.update_change_password()
            self.user.save()
        return self.user