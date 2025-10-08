# TODO: Delete this entire file - all code is commented out and serializers are implemented in apps/user/serializers.py
# If this was an alternative implementation, either use it or remove it completely

# from django.contrib.auth import authenticate, get_user_model
# from django.utils.translation import gettext as _
# from rest_framework import exceptions, serializers
# from rest_framework_simplejwt.serializers import (
#     TokenObtainSerializer,
#     api_settings,
#     update_last_login,
# )

# from .backend import CustomRefreshToken


# class EmailLoginSerializer(TokenObtainSerializer):
#     username_field = get_user_model().EMAIL_FIELD

#     @classmethod
#     def get_token(cls, user):
#         return CustomRefreshToken.for_user(user)

#     def validate(self, attrs):
#         authenticate_kwargs = {
#             "username": attrs[self.username_field],
#             "password": attrs["password"],
#             "raise_api_exception": True,
#         }

#         if "request" in self.context:
#             authenticate_kwargs["request"] = self.context["request"]

#         self.user = authenticate(**authenticate_kwargs)

#         if not api_settings.USER_AUTHENTICATION_RULE(self.user):
#             raise exceptions.AuthenticationFailed(
#                 self.error_messages[_("no_active_account")],
#                 "no_active_account",
#             )

#         data = {}
#         refresh = self.get_token(self.user)

#         data["refresh"] = str(refresh)
#         data["access"] = str(refresh.access_token)

#         if api_settings.UPDATE_LAST_LOGIN:
#             update_last_login(None, self.user)

#         return data


# class EmailLoginResponseSerializer(serializers.Serializer):
#     refresh = serializers.CharField(read_only=True)
#     access = serializers.CharField(read_only=True)
