import json
from django.contrib.messages.middleware import MessageMiddleware
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.encoding import force_str
from django.utils.functional import Promise


class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_str(obj)
        return super().default(obj)


class CustomResponse(MessageMiddleware):
    def process_response(self, request, response):
        # Bypass response processing for non-API requests (e.g., OpenAPI schema,
        # static files, admin interface) to preserve their original response format
        normalized_path = request.path.replace("//", "/")
        if not normalized_path.startswith("/api/"):
            return response

        code = response.status_code
        response = super().process_response(request, response)

        if response.headers.get("Content-Type") != "application/json":
            return response

        request_path = request.path.split("/")
        request_path = list(filter(None, request_path))

        if code not in [400, 401, 403, 404, 500, 501]:
            interceptor = {
                "error": False,
                "code": response.status_code,
                "message": None,
                "data": None,
            }

            if hasattr(response, "data"):
                response_data = response.data

                # move detail from data to the "detail" key
                if "detail" in response_data:
                    interceptor["message"] = response_data.pop("detail")

                # For list-based views, add count, next and previous keys
                # and set the 'data' property of the interceptor to the results
                if request.method == "GET":
                    count = response_data.get("count", None)
                    next = response_data.get("next", None)
                    previous = response_data.get("previous", None)
                    results = response_data.get("results", None)
                    extra_data = response_data.get("extra_data", None)
                    if results is not None and count is not None:
                        interceptor["data"] = results
                        interceptor["count"] = count
                        interceptor["next"] = next
                        interceptor["previous"] = previous
                        interceptor["extra_data"] = extra_data
                    else:
                        interceptor["data"] = response.data
                else:
                    interceptor["data"] = response.data

                # If the 'data' property of the interceptor is an empty dict,
                # then set it to None
                if isinstance(interceptor["data"], dict) and not interceptor["data"]:
                    interceptor["data"] = None

        else:
            
            if not response.data.get("message", None):
                detail = json.loads(response.content.decode()).get("data", None)
                if isinstance(detail, dict):
                    response_detail = tuple(detail)[0] if detail else detail
                elif isinstance(detail, list):
                    response_detail = detail[0]
                else:
                    response_detail = detail
                interceptor = {
                    "error": True,
                    "code": 401 if detail == "Token is invalid or expired" else response.status_code,
                    "message": response_detail,
                    "data": response.data.get("data", None),
                }
            else:
                interceptor = response.data
        response.data = interceptor
        response.content = json.dumps(interceptor, cls=LazyEncoder).encode()
        response.status_code = 401 if interceptor["message"] == "Token is invalid or expired" else code
        return response
