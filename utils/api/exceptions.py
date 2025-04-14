from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.exceptions import APIException

"""
DEPRECATED: We dont use this file anymore.
"""


# ------------------------------ Authentication ------------------------------ #
class AuthenticationFailed(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _("Login failed, please check your email or password again.")
    default_code = "authentication_failed"


# -------------------------------- Third party ------------------------------- #
class ServiceUnavailable(APIException):
    """Third party API service is unavailable"""

    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = _("Service unavailable, please check again later.")
    default_code = "service_unavailable"
