# import json

# from django.conf import settings
# from django.http.response import JsonResponse

# from utils.api.exceptions import ServiceUnavailable


# class CutOffMiddleware:
#     def get_parameters(self):
#         raw_data = open(  # noqa: UP015, SIM115
#             f"{settings.BASE_DIR}/cut-off-parameters.json", "r"
#         ).read()  # noqa: UP015, SIM115
#         response = json.loads(raw_data)
#         return response

#     def build_response(self) -> JsonResponse:
#         response_status_code = ServiceUnavailable.status_code
#         response_headers = {"Cache-Control": "no-store"}
#         response_data = {
#             "error": True,
#             "code": response_status_code,
#             "messages": ServiceUnavailable.default_detail,
#             "data": {},
#         }

#         return JsonResponse(
#             response_data,
#             headers=response_headers,
#             status=response_status_code,
#         )

#     def __init__(self, get_response):
#         self.get_response = get_response
#         # One-time configuration and initialization.

#     def __call__(self, request):
#         # Code to be executed for each request before
#         # the view (and later middleware) are called.

#         data = self.get_parameters()
#         host = request.path.split("/")
#         if "v1" in host:
#             path_url = data.get(host[3], None)
#             if path_url is False:
#                 service_unavailable = self.build_response()
#                 return service_unavailable

#         response = self.get_response(request)

#         # Code to be executed for each request/response after
#         # the view is called.

#         return response
