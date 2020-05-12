from django.shortcuts import render


def home_view(request):
    return render(request, "home/index.html", {"include_bundle": "browser"})
