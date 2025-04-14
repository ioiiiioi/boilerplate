from django.urls import include, path

from .redirection import redirect_docs

urlpatterns = [
    path("", redirect_docs),
    path("auth/", include("apps.user.urls")),
]
