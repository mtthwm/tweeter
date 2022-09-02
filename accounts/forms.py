from django import forms
from django.forms import ModelForm
from homepage.models import User
from django.forms import ValidationError

class SignInForm(forms.Form):
    username = forms.CharField(max_length=150, label=False)
    password = forms.CharField(widget=forms.PasswordInput(), label=False)

    username.widget.attrs.update({"class": "form-default sign-in-input w-100", "placeholder": "Username"})
    password.widget.attrs.update({"class": "form-default sign-in-input w-100 mt-5", "placeholder": "Password"})


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=150, label=False)
    password = forms.CharField(widget=forms.PasswordInput(), label=False)
    password_conf = forms.CharField(widget=forms.PasswordInput(), label=False)

    username.widget.attrs.update({"class": "form-default form-light sign-in-input w-100", "placeholder": "Username"})
    password.widget.attrs.update({"class": "form-default form-light sign-in-input w-100 mt-5", "placeholder": "Password"})
    password_conf.widget.attrs.update({"class": "form-default form-light sign-in-input w-100 mt-5", "placeholder": "Password (Again)"})

    def clean (self):
        cleaned_data = super().clean()
        if not cleaned_data.get("password") == cleaned_data.get("password_conf"):
            raise ValidationError("Passwords do not match")
        if User.objects.filter(username=cleaned_data.get("username")).exists():
            raise ValidationError("Username already exists")