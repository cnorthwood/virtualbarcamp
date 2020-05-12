from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpRequest
from django.shortcuts import redirect, render

from virtualbarcamp.home.models import GlobalSettings


def register_view(request: HttpRequest):
    registration_open = GlobalSettings.objects.get().allow_registration
    if registration_open:
        if request.method == "POST":
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get("username")
                raw_password = form.cleaned_data.get("password1")
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect("home")
        else:
            form = UserCreationForm()
        return render(
            request, "registration/register.html", {"form": form, "include_bundle": "accounts"}
        )
    else:
        return render(
            request, "registration/registration_not_open.html", {"include_bundle": "accounts"}
        )
