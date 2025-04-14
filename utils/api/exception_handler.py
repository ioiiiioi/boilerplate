import logging

from rest_framework.response import Response
from rest_framework.exceptions import ErrorDetail
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.views import exception_handler
# from sentry_sdk import capture_exception


def detailed_exception_handler(exc, context):
    # TODO: maybe move this to a different logger
    logger = logging.getLogger("django.request")
    logger.exception(exc)
    # capture_exception(exc)

    response = exception_handler(exc, context)

    # default error if response is None
    code = HTTP_500_INTERNAL_SERVER_ERROR
    detail = str(exc)
    data = None

    if response:
        code = response.status_code

        # if the error has detail, put it in the "detail" key
        # and put the rest of the data in the "data" key
        detail = response.data.pop("detail") if "detail" in response.data else None
        data = response.data or None

    if isinstance(detail, list):
        detail = detail[0]

    if isinstance(detail, ErrorDetail):
        detail = detail.__str__()

    response = {
        "error": True,
        "code": 401 if detail == "Token is invalid or expired" else code,
        "message": detail,
        "data": data,
    }
    return Response(response, status=code)
