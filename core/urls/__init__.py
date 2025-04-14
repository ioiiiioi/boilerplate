"""django_boilerplate_noble URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path, re_path, reverse
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from .redirection import redirect_docs


# drf-spectacular for swagger
urlpatterns = [
    path(
        "v1/schema/", SpectacularAPIView.as_view(api_version="v1"), name="schemav1"
    ),
    path(
        "v1/docs/",
        lambda request: render(
            request,
            "scalar/scalar.html",
            {"schema_url": reverse("schemav1")},
        ),
        name="scalar-ui",
    ),
    path(
        "v1/swagger/",
        SpectacularSwaggerView.as_view(url_name="schemav1"),
        name="swagger-ui",
    ),
]

urlpatterns += [
    path("", redirect_docs),
    # path("ckeditor/", include("ckeditor_uploader.urls")),
    path("v1/admin/", admin.site.urls),
    path("api/v1/", include("core.urls.v1")),
]

if "rosetta" in settings.INSTALLED_APPS:
    urlpatterns += [re_path(r"^rosetta/", include("rosetta.urls"))]
