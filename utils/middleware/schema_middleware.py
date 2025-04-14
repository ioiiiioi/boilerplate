import random

from drf_spectacular.openapi import AutoSchema
from rest_framework import serializers


def generate_serializer_dummy_values(serializer):
    """
    Generates dummy values for fields in a serializer based on their data type.
    Args:
        serializer (serializers.Serializer): The serializer instance.
    Returns:
        dict: A dictionary containing field names as keys and dummy values as values.
    """
    dummy_values = {}
    for field_name, field in serializer.fields.items():
        field_type = type(field).__name__
        if field.write_only:
            continue

        if field_type in ["CharField", "TextField"]:
            dummy_values[field_name] = f"dummy_{field_name}"

        elif field_type == "ChoiceField":
            dummy_values[field_name] = random.choice(list(dict(field.choices).keys()))

        elif field_type == "UUIDField":
            dummy_values[field_name] = "f8a5b5c7-5f9d-4e8b-9c4f-4b4b4b4b4b4b"

        elif field_type == "SerializerMethodField":
            dummy_values[field_name] = "Could be string or integer depends on the data."

        elif field_type == "SlugField":
            dummy_values[field_name] = "dummy-slug"

        elif field_type == "URLField":
            dummy_values[field_name] = "https://example.com"

        elif field_type == "EmailField":
            dummy_values[field_name] = "dummy@example.com"

        elif field_type == "IntegerField":
            dummy_values[field_name] = 39

        elif field_type == "FloatField":
            dummy_values[field_name] = 1.12

        elif field_type == "DecimalField":
            dummy_values[field_name] = 2.12

        elif field_type == "BooleanField":
            dummy_values[field_name] = True

        elif field_type == "DateField":
            dummy_values[field_name] = "2023-04-10"

        elif field_type == "DateTimeField":
            dummy_values[field_name] = "2023-04-10T00:00:00Z"

        elif field_type == "TimeField":
            dummy_values[field_name] = "12:00:00"

        elif field_type == "ListField":
            dummy_values[field_name] = [1, 2, 3]

        elif field_type == "DictField":
            dummy_values[field_name] = {"key": "value"}

        elif field_type == "ListSerializer":
            dummy_values[field_name] = [{"key1": "value1"}, {"key2": "value2"}]

        elif field_type == "ArrayField":
            dummy_values[field_name] = [1, 2, 3]

        elif field_type == "JSONField":
            dummy_values[field_name] = {"key": "value"}

        elif field_type == "PrimaryKeyRelatedField":
            dummy_values[field_name] = 1

        elif field_type == "ManyRelatedField":
            dummy_values[field_name] = [1, 2]

        ## handle for file field
        elif field_type == "FileField":
            dummy_values[field_name] = f"https:/storage.service.url/dummy.txt"

        elif field_type == "ImageField":
            dummy_values[field_name] = f"https:/storage.service.url/dummy.png"

        ## handle for nested related serializer
        elif isinstance(field, serializers.Serializer):
            dummy_values[field_name] = generate_serializer_dummy_values(field)

        else:
            dummy_values[field_name] = None

    return dummy_values


class CustomAutoSchema(AutoSchema):
    def __init__(self, _api_type=None):
        super().__init__()
        self.__api_type = None
        if _api_type:
            self.__api_type = _api_type

    def _get_response_bodies(self, direction="response"):
        serializer = self.get_response_serializers()
        response_bodies = {}
        examples = None
        if isinstance(serializer, dict):
            # custom handling for overriding default return codes with @extend_schema
            for code, serializer_resp in serializer.items():
                if isinstance(code, tuple):
                    code, media_types = str(code[0]), code[1:]
                else:
                    code, media_types = str(code), None
                content_response = self._get_response_for_code(
                    serializer_resp, code, media_types, direction
                )
                if code in response_bodies:
                    response_bodies[code]["content"].update(content_response["content"])
                else:
                    response_bodies[code] = content_response
            # return response_bodies

        if not response_bodies:
            response_bodies = super()._get_response_bodies(direction)
            media_type = (
                response_bodies.get("200", {})
                .get("content", {})
                .get("application/json", {})
            )
            examples = media_type.get("examples", {})

        if not examples and serializer and (not isinstance(serializer, dict)):
            match self.method:
                case "GET":
                    dummy_values = generate_serializer_dummy_values(serializer)
                    media_type["examples"] = {
                        "ResponseData": {
                            "value": {
                                "code": 200,
                                "status": "sucess / error",
                                "message": "",
                                "data": (
                                    [dummy_values]
                                    if self.__api_type == "List"
                                    else dummy_values
                                ),
                                "extra_data": {},
                            },
                            "summary": "Response Data",
                            "description": f"This is response data for {self.path}",
                        }
                    }
                    if self.__api_type == "List":
                        pagination_detail = {
                            "count": 1,
                            "next": "https://domain.service.url/endpoint/page=page_num",
                            "previous": "https://domain.service.url/endpoint/page=page_num",
                        }
                        media_type["examples"]["ResponseData"][
                            "value"
                        ] |= pagination_detail
                    response_bodies["200"]["content"]["application/json"] = media_type
                case "DELETE":
                    media_type["examples"] = {
                        "ResponseData": {
                            "value": {
                                "code": 200,
                                "status": "sucess / error",
                                "message": "Object with ID 1 was deleted.",
                                "data": {},
                                "extra_data": {},
                            },
                            "summary": "Response Data",
                            "description": f"This is response data for {self.path}",
                        }
                    }
                    response_bodies = {
                        "200": {"content": {"application/json": media_type}}
                    }
                case "POST":
                    media_type["examples"] = {
                        "ResponseData": {
                            "value": {
                                "code": 201,
                                "status": "sucess / error",
                                "message": None,
                                "data": generate_serializer_dummy_values(serializer),
                                "extra_data": {},
                            },
                            "summary": "Response Data",
                            "description": f"This is response data for {self.path}",
                        }
                    }
                    # if (
                    #     response_bodies.get("201", None)
                    #     and response_bodies["201"].get("content", None)
                    #     and response_bodies["201"]["content"].get(
                    #         "application/json", None
                    #     )
                    #     and response_bodies["201"]["content"]["application/json"].get(
                    #         "examples"
                    #     )
                    # ):
                    #     response_bodies["201"]["content"]["application/json"][
                    #         "examples"
                    #     ]["DefaultResponse"] = media_type["examples"]["ResponseData"]
                    # else:
                    response_bodies = {
                        "201": {"content": {"application/json": media_type}}
                    }
                case "PATCH":
                    dummy_values = generate_serializer_dummy_values(serializer)
                    media_type["examples"] = {
                        "ResponseData": {
                            "value": {
                                "code": 200,
                                "status": "sucess",
                                "message": "",
                                "data": dummy_values,
                                "extra_data": {},
                            },
                            "summary": "Response Data",
                            "description": f"This is response data for {self.path}",
                        }
                    }
                    response_bodies = {
                        "200": {"content": {"application/json": media_type}}
                    }
        else:
            pass

        response_bodies = self._get_error_response(response_bodies)
        return response_bodies

    def _get_error_response(self, response_bodies):
        response = {
            "examples": {
                "ResponseData": {
                    "value": {
                        "status": "error",
                        "code": 401,
                        "message": "Signature verification failed",
                        "data": None,
                    },
                    "summary": "Signature verification failed",
                    "description": "This response indicate the Access Token has been exipred.",
                },
                "ResponseData2": {
                    "value": {
                        "status": "error",
                        "code": 401,
                        "message": "Need access token.",
                        "data": None,
                    },
                    "summary": "Access token missing",
                    "description": "This response indicate Access Token was not on the headers.",
                },
            }
        }
        response_bodies["401"] = {"content": {"application/json": response}}
        response = {
            "examples": {
                "ResponseData": {
                    "value": {
                        "status": "error",
                        "code": 500,
                        "message": "Somthing wrong with API",
                        "data": None,
                    },
                    "summary": "Internal error",
                    "description": "This response indicate error on the BE code or Data confilct due to testing.",
                }
            }
        }
        response_bodies["500"] = {"content": {"application/json": response}}
        response = {
            "examples": {
                "ResponseData": {
                    "value": {
                        "status": "error",
                        "code": 404,
                        "message": "Not found.",
                        "data": None,
                    },
                    "summary": "Data not found",
                    "description": "This response indicate data was't found on DB.",
                }
            }
        }
        response_bodies["404"] = {"content": {"application/json": response}}
        return response_bodies
