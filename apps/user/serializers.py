from collections import OrderedDict
from datetime import datetime
from typing import Any, Dict
from django.contrib.auth import authenticate
from django.core.cache import cache
from django.db.models import Prefetch
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from core.auth.backend import CustomRefreshToken
from .models import (
    User,
)


class LoginSerializerV2(serializers.Serializer):
    login = serializers.CharField(required=False, allow_null=True, write_only=True)
    email = serializers.CharField(required=False, allow_null=True)
    password = serializers.CharField(write_only=True)
    jwt = serializers.JSONField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)
    gender = serializers.CharField(read_only=True)  # TODO: Remove - User model doesn't have gender field

    def login_with_email(
        self, email: str, password: str, school_id: int = None
    ) -> User:
        # TODO: Remove school_id parameter - User model doesn't have school relation in boilerplate
        authenticate_kwargs = {
            "email": email,
            "password": password,
            "raise_api_exception": True,
            "username": None,
            "school": school_id,  # TODO: Remove this - not used in boilerplate
            "user_type": None,  # TODO: Remove this - not used in boilerplate
        }

        if "request" in self.context:
            authenticate_kwargs["request"] = self.context["request"]

        user = authenticate(**authenticate_kwargs)
        return user

    def login_with_username(
        self, user: str, password: str
    ) -> User:
        authenticate_kwargs = {
            "username": user,
            "password": password,
            "raise_api_exception": True,
            "user_type": None,
        }

        if "request" in self.context:
            authenticate_kwargs["request"] = self.context["request"]

        user = authenticate(**authenticate_kwargs)
        return user

    def validate(self, attrs):
        username = attrs.get("login", None)
        email = attrs.get("email", None)
        school_id = attrs.get("school_id", None)  # TODO: Remove - not used in boilerplate
        password = attrs.get("password")

        if password in ["", " ", None, "null"]:
            raise exceptions.NotAuthenticated("invalid_username_password")

        if email:
            user = self.login_with_email(email, password)
        else:
            user = self.login_with_username(username, password)
        attrs["user"] = user
        return attrs

    def create(self, validated_data):
        return validated_data.get("user")

    def to_representation(self, instance):

        ret = OrderedDict()
        refresh = CustomRefreshToken.for_user(instance)
        ret["jwt"] = {
            "refresh": refresh.__str__(),
            "access": refresh.access_token.__str__(),
        }
        ret["detail"] = "Login sucessful"
        ret["id"] = instance.id
        ret["username"] = instance.username
        ret["email"] = instance.email
        ret["name"] = instance.get_full_name()
        ret["google_info"] = self.add_google_info(instance)  # TODO: Define add_google_info method or remove this line
        ret["last_login"] = (
            instance.last_login.strftime("%Y-%m-%dT%H:%M:%S%z")
            if isinstance(instance.last_login, datetime)
            else instance.last_login
        )
        ret["status"] = "success"
        ret["is_staff"] = instance.is_staff
        # ret["picture"] = self.user_picture(),  # TODO: Uncomment and fix or remove completely
        
        return ret
   
    # TODO: Delete user_picture method if not needed, or uncomment and fix the implementation
    # def user_picture(self, profile):
    #     print(profile.picture, "<---- PIC")
    #     return (
    #         profile.picture.url
    #         if profile.picture and not isinstance(profile.picture, str)
    #         else None
    #     )


class RefreshTokenSerializer(TokenRefreshSerializer):
    token_class = CustomRefreshToken

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        refresh = self.token_class(attrs["refresh"])

        data = {"access": str(refresh.access_token)}
        refresh.set_exp()
        refresh.set_iat()

        data["refresh"] = str(refresh)

        return data

    def create(self, validated_data):
        return validated_data

    def to_representation(self, instance):
        ret = {"access": instance.get("access").__str__()}
        return ret


class LogoutSerializerV2(serializers.Serializer):

    def create(self, validated_data):
        request = self.context.get("request")
        cache.delete_pattern(f"token:{request.user.id}:*")
        cache.delete_pattern(f"user:{request.user.id}*")
        return validated_data

    def to_representation(self, instance):
        return {"detail": "Logout successful"}

