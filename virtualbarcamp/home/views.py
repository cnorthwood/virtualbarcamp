from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from virtualbarcamp.accounts.decorators import user_has_accepted_code_of_conduct


@login_required
@user_has_accepted_code_of_conduct
def home_view(request):
    return render(request, "home/index.html", {"include_bundle": "browser"})
