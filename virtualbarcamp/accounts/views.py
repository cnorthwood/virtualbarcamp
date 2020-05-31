from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from virtualbarcamp.accounts.forms import AcceptCodeOfConductForm
from virtualbarcamp.accounts.models import Account


def login(request):
    return render(request, "registration/login.html", {"include_bundle": "accounts"})


@login_required
def accept_code_of_conduct(request):
    if (
        hasattr(request.user, "account")
        and request.user.account.has_accepted_code_of_conduct is not None
    ):
        return redirect("home")

    if request.method == "POST":
        form = AcceptCodeOfConductForm(request.POST)
        if form.is_valid():
            Account.objects.get_or_create(
                user=request.user, has_accepted_code_of_conduct=datetime.now()
            )
            return redirect("home")
    else:
        form = AcceptCodeOfConductForm()

    return render(
        request,
        "registration/accept_code_of_conduct.html",
        {"form": form, "include_bundle": "accounts"},
    )
