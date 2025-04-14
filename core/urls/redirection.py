from django.shortcuts import redirect, reverse


def redirect_docs(request):
    return redirect(reverse("scalar-ui"))