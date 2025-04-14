from apps.user.models import User
from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.base.base_views import CreateAPIView
from .serializers import (
    LoginSerializerV2,
    LogoutSerializerV2,
    RefreshTokenSerializer,
)


class LoginView(CreateAPIView):
    serializer_class = LoginSerializerV2
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        request.version = "v2"
        res = super().post(request, *args, **kwargs)
        return res


class RefreshTokenView(CreateAPIView):
    serializer_class = RefreshTokenSerializer
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        request.version = "v2"
        return super().post(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=200, headers=headers)


class LogoutView(CreateAPIView):
    serializer_class = LogoutSerializerV2
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.version = "v2"
        return super().post(request, *args, **kwargs)
