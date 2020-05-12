from django.contrib.auth import views as authviews
from django.urls import path

from virtualbarcamp.accounts.views import register_view

urlpatterns = [
    path("register/", register_view, name="register",),
    path(
        "login/",
        authviews.LoginView.as_view(extra_context={"include_bundle": "accounts"}),
        name="login",
    ),
    path("logout/", authviews.logout_then_login, name="logout",),
    path(
        "change-password/",
        authviews.PasswordChangeView.as_view(
            extra_context={"include_bundle": "accounts"},
            template_name="registration/change-password.html",
            success_url="/",
        ),
        name="password_change",
    ),
    path(
        "reset-password/",
        authviews.PasswordResetView.as_view(
            extra_context={"include_bundle": "accounts"},
            template_name="registration/reset-password.html",
        ),
        name="password_reset",
    ),
    path(
        "reset-password/done/",
        authviews.PasswordResetDoneView.as_view(
            extra_context={"include_bundle": "accounts"},
            template_name="registration/reset-password-done.html",
        ),
        name="password_reset_done",
    ),
    path(
        "reset-password/<uidb64>/<token>/",
        authviews.PasswordResetConfirmView.as_view(
            extra_context={"include_bundle": "accounts"},
            template_name="registration/reset-password-confirm.html",
            success_url="/",
        ),
        name="password_reset_confirm",
    ),
]
