from django.shortcuts import render
from django.views import View
from homepage.models import User
from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login
from .forms import SignInForm, SignUpForm

# Create your views here.
class SignInView(View):
    # TODO: PROPER ERROR HANDLING
    def get (self, request, **kwargs):
        if request.user.is_authenticated:
            print("authenticated", request.META.get('HTTP_REFERER'))
            return HttpResponseRedirect(f'/user/{request.user.username}')
        
        context = {
            "signInForm": SignInForm(),
            "signUpForm": SignUpForm()
        }
        return render(request, "accounts/sign_in.html", context)

    def post (self, request, **kwargs):
        # TODO: PROPER ERROR HANDLING
        try:
            form = SignInForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password")

                user = authenticate(request, username=username, password=password)
                if user:
                    login(request, user)
                    return HttpResponseRedirect(f'/user/{username}')
                else:
                    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

            else:
                print("FORM NOT VALID")
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

        except Exception as e:
            print("EXCEPTION", e)
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))




class SignUpView(View):
    def get (self, request, **kwargs):
        return HttpResponseRedirect("/accounts/sign_in")

    def post (self, request, **kwargs):
        # TODO: PROPER ERROR HANDLING
        try:
            form = SignUpForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password")

                u = User()
                u.username = username
                u.password = password
                u.save()
                login(request, u)
                return HttpResponseRedirect(f'/user/{username}')
            
            else:
                print("FORM NOT VALID")
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

        except Exception as e:
            print("EXCEPTION", e)
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

      