# from django.contrib.auth import logout
# from django.utils.translation import gettext as _
# from drf_spectacular.utils import OpenApiResponse, extend_schema
# from rest_framework import status
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.request import Request
# from rest_framework.response import Response
# from rest_framework_simplejwt.views import TokenObtainPairView

# from core.auth.backend import UserAuthorization

# from .serializers import EmailLoginResponseSerializer, EmailLoginSerializer


# class EmailTokenObtainPairView(TokenObtainPairView):
#     serializer_class = EmailLoginSerializer

#     @extend_schema(
#         request=EmailLoginSerializer,
#         responses={
#             200: OpenApiResponse(
#                 response=EmailLoginResponseSerializer,
#                 description="Logged in successfully",
#             ),
#             400: OpenApiResponse(description="Authentication failed"),
#         },
#     )
#     def post(self, request: Request, *args, **kwargs) -> Response:
#         return super().post(request, *args, **kwargs)


# @extend_schema(responses={200: OpenApiResponse(description="Logged out successfully")})
# @api_view(["POST"])
# @permission_classes([IsAuthenticated])
# def logout_view(request) -> Response:
#     # blacklist old token
#     authorization = UserAuthorization()
#     authorization.blacklist_token(request)

#     # log the user out
#     logout(request)

#     return Response({"detail": _("User has been logout")}, status=status.HTTP_200_OK)
