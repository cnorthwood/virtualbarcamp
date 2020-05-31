from django.shortcuts import redirect


def user_has_accepted_code_of_conduct(f):
    def check_code_of_conduct_acceptance(request):
        if (
            not hasattr(request.user, "account")
            or request.user.account.has_accepted_code_of_conduct is None
        ):
            return redirect("accept_code_of_conduct")
        return f(request)

    return check_code_of_conduct_acceptance
