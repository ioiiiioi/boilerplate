import uuid
import json
import contextlib
from django.core.cache import cache
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework import exceptions
from rest_framework.exceptions import AuthenticationFailed, ValidationError, PermissionDenied
from rest_framework_simplejwt.tokens import AccessToken, Token
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.serializers import ModelSerializer


USER = get_user_model()
DEFAULT_CACHE = cache

class CacheUserSlimSerializer(ModelSerializer):
    """
    CacheUserSlimSerializer is a serializer for the USER model that provides
    serialization and deserialization of user data, including caching functionality.
    Attributes:
        json (property): Returns the serialized data in JSON format with indentation.
    Methods:
        from_cache(cls, data):
            Class method that deserializes the given JSON string `data` and retrieves
            the corresponding user instance from the database. If the user is not found
            or multiple users are returned, it raises an AuthenticationFailed exception.
        Meta:
            model (USER): The model that is being serialized.
            fields (list): List of fields to be included in the serialized output.
    """

    @property
    def json(self):
        return json.dumps(self.data, indent=4)
    
    @classmethod
    def from_cache(cls, data):
        data_dict = json.loads(data)
        with contextlib.suppress(ObjectDoesNotExist, MultipleObjectsReturned):
            instance = cls.Meta.model.objects.get(id=data_dict.get("id"))
            return instance
        raise AuthenticationFailed("user_not_found_or_invalid_school_id", code="user_not_found")

    class Meta:
        model = USER
        fields = [
            "id"
            "username",
            "first_name",
            "last_name",
            "email",
            "is_staff",
            "is_active",
            "date_joined",
        ]

class CustomBlacklistMixins:
    """
    A mixin class that provides custom blacklist functionality for token verification and user authentication.
    Methods:
    --------
    verify(*args, **kwargs):
        Verifies the token by checking if it is blacklisted and then calls the parent class's verify method.
    check_blacklist():
        Checks if the token is blacklisted by looking it up in the cache. Raises an InvalidToken exception if the token is blacklisted.
    for_user(cls, user):
        Generates a token for the given user, adds custom claims, and stores the token and user information in the cache. 
        Handles single login by deleting previous tokens for the user. Updates the user's last login time and saves the user.
    blacklist():
        Blacklists the token by deleting the user and token information from the cache.
    """
    def verify(self, *args, **kwargs):
        self.check_blacklist()
        super().verify(*args, **kwargs)

    def check_blacklist(self):
        jti = self.payload[api_settings.JTI_CLAIM]
        user_id = self.payload["user_id"]

        if not DEFAULT_CACHE.get(f"token:{user_id}:{jti}"):
            raise InvalidToken(_("Token is blacklisted"))

    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)  # type: ignore

        token["x-auth-services-num"] = str(uuid.uuid4().hex)
        if user.school:
            token["school_id"] = user.school.id
        
        if settings.IS_SINGLE_LOGIN:
            DEFAULT_CACHE.delete_pattern(f"token:{user.id}:*")
        
        DEFAULT_CACHE.set(
            f"user:{user.id}", 
            CacheUserSlimSerializer(user).json, 
            int(api_settings.REFRESH_TOKEN_LIFETIME.total_seconds())
        )
        DEFAULT_CACHE.set(
            key=f"token:{user.id}:{token['jti']}",
            value=token,
            timeout=int(api_settings.REFRESH_TOKEN_LIFETIME.total_seconds()),
        )
        user.last_login = timezone.now()
        user.session_login_id = None
        user.save()
        return token

    def blacklist(self):
        jti = self.payload[api_settings.JTI_CLAIM]
        user_id = self.payload["user_id"]
        DEFAULT_CACHE.delete(f"user:{user_id}")
        return DEFAULT_CACHE.delete_pattern(f"token:{user_id}*")

class CustomRefreshToken(CustomBlacklistMixins, Token):
    """
    CustomRefreshToken class that extends CustomBlacklistMixins and Token.

    This class represents a custom refresh token with specific properties and methods
    to handle token claims and access token generation.

    Attributes:
        no_copy_claims (tuple): Claims that should not be copied to the access token.
        token_type (str): Type of the token, set to "refresh".
        lifetime (datetime.timedelta): Lifetime of the refresh token.
        access_token_class (class): Class used to generate access tokens.

    Properties:
        access_token (AccessToken): Generates and returns an access token with claims
                                    copied from the refresh token, excluding those in
                                    no_copy_claims.
    """
    no_copy_claims = (
        api_settings.TOKEN_TYPE_CLAIM,
        "exp",
    )
    token_type = "refresh"
    lifetime = api_settings.REFRESH_TOKEN_LIFETIME
    access_token_class = AccessToken

    @property
    def access_token(self):
        access = self.access_token_class()
        access.set_exp(from_time=self.current_time)

        no_copy = self.no_copy_claims
        for claim, value in self.payload.items():
            if claim in no_copy:
                continue
            access[claim] = value

        return access

class CustomAccessToken(CustomRefreshToken):
    token_type = "access"

class NewAuthentication:
    """
    A class used to handle user authentication.
    Methods
    -------
    user_instance(params)
        Retrieves a user instance based on the provided parameters.
    get_user_new(validated_token)
        Retrieves a user based on the validated token and checks the user's session and activity status.
    
        Retrieves a user instance based on the provided parameters.
        Parameters
        ----------
        params : dict
            A dictionary of parameters to filter the user.
        Returns
        -------
        user : USER
            The user instance that matches the provided parameters.
        Raises
        ------
        AuthenticationFailed
            If no user is found or multiple users are returned.

        Retrieves a user based on the validated token and checks the user's session and activity status.
        Parameters
        ----------
        validated_token : dict
            A dictionary containing the validated token information.
        Returns
        -------
        user : USER
            The user instance that matches the validated token.
        Raises
        ------
        AuthenticationFailed
            If the session is terminated or the user is inactive.
        """

    def user_instance(self, params):
        with contextlib.suppress(ObjectDoesNotExist, MultipleObjectsReturned):
            user = USER.objects.get(**params)
            return user
        raise AuthenticationFailed("user_not_found_or_invalid_school_id", code="user_not_found")
   
    def get_user_new(self, validated_token):
        if not cache.get(f"token:{validated_token.get('user_id')}:{validated_token.get('jti')}"):
            raise AuthenticationFailed(_("This session is terminated because of new login into different device or browser."), code="session_expired")

        user_cache = cache.get(f"user:{validated_token.get('user_id')}")
        if not user_cache:
            params = {api_settings.USER_ID_FIELD: validated_token.get('user_id')}
            user = self.user_instance(params)
        else:
            user = CacheUserSlimSerializer.from_cache(user_cache)
      
        if not user.is_active:
            raise AuthenticationFailed("user_blocked", code="user_inactive")
    
        return user

class CustomJWTAuthentication(JWTAuthentication, NewAuthentication):
    def get_user(self, validated_token):
        return self.get_user_new(validated_token)

class AuthenticateNewMixins:
    """
    A mixin class that provides methods for authenticating users and handling errors.
    Methods
    -------
    error_raiser(host, err_msg: str = None):
        Raises appropriate authentication or validation errors based on the host.
    __get_user(host, params):
        Retrieves a user from the database based on the provided parameters and caches the user.
        Raises an error if the user is not found or multiple users are returned.
    authenticate_new(request=None, username=None, email=None, password=None, school=None, user_type=None, **kwargs):
        Authenticates a user based on the provided credentials and additional parameters.
        Performs various checks to ensure the user can be authenticated and raises errors if any checks fail.
    """
    def error_raiser(self, host, err_msg: str = None):
        if "api" in host:
            if err_msg:
                raise AuthenticationFailed(err_msg)
            raise AuthenticationFailed() from None
        else:
            if err_msg:
                raise ValidationError(err_msg)
            raise ValidationError("invalid_username_password") from None

    def __get_user(self, host, params):
        with contextlib.suppress(ObjectDoesNotExist, MultipleObjectsReturned):
            user = USER.objects.get(**params)
            cache.set(
                f"user:{user.id}", 
                user,
                int(api_settings.REFRESH_TOKEN_LIFETIME.total_seconds())
            )
            return user
        err_msg = "invalid_username_password"
        self.error_raiser(host, err_msg)

    def authenticate_new(self, request=None, username=None, email=None, password=None, school=None, user_type=None, **kwargs):
        host = request.get_full_path().split("/")
        
        filter_params = {}
        if username:
            filter_params["username"] = username

        if not filter_params and email:
            filter_params["email__iexact"] = email
        
        if not filter_params:
            err_msg = _("Email or Username required.")
            raise self.error_raiser(host, err_msg)

        user = self.__get_user(host, filter_params)

        if not "api" in host:
            return user

        # if user.user_type is None:
        #     raise PermissionDenied("user_type_not_set.")

        # if user.user_type not in [
        #     "official1",
        #     "official2",
        #     "foundation",
        #     "college_user",
        #     "applicant",
        # ]:
        #     if not school:
        #         err_msg = "school_id_required"
        #         raise self.error_raiser(host, err_msg)

        #     if school and user.school.id != int(school):
        #         err_msg = "user_not_found_or_invalid_school_id"
        #         self.error_raiser(host, err_msg)
        # else:
        #     if school:
        #         err_msg = "invalid_login_form"
        #         self.error_raiser(host, err_msg)
        
        if not user.check_password(password):
            err_msg = "invalid_username_password"
            self.error_raiser(host, err_msg)

        if user.is_deleted:
            err_msg = "user_has_been_deleted"
            self.error_raiser(host, err_msg)
        
        if not self.user_can_authenticate(user):
            err_msg = "user_blocked"
            self.error_raiser(host, err_msg)

        return user

class CustomAuthBackend(AuthenticateNewMixins, ModelBackend):
    def authenticate(self, request=None, username=None, email=None, password=None, school=None, user_type=None, **kwargs):
        return super().authenticate_new(request, username, email, password, school, user_type, **kwargs)
    
    def user_can_authenticate(self, user):
        return super().user_can_authenticate(user)

class UserAuthorization(TokenAuthentication, NewAuthentication):
    """
    UserAuthorization class for handling token-based user authentication.
    Attributes:
        keyword (str): The keyword used for token authentication.
        user_model (Model): The user model used for authentication.
    Methods:
        get_raw_token(request) -> bytes | None:
            Extracts the raw token from the request headers.
        can_skip(request) -> bool:
            Determines if the request can skip authentication based on the request path.
        is_logout(request) -> bool:
            Checks if the request is a logout request based on the request path.
        authenticate(request):
            Authenticates the user based on the provided token in the request.
    """
    keyword = "Bearer"
    user_model = get_user_model()

    def get_raw_token(self, request) -> bytes | None:
        headers = request.headers
        authorization = headers.get("Authorization", None)

        if not authorization or len(authorization.split()) != 2:
            raise exceptions.NotAuthenticated(detail=_("Need access token."))

        keyword, token = authorization.split()
        if keyword.lower() != self.keyword.lower():
            raise AuthenticationFailed(detail=_("Wrong token scheme."))

        if not token or token == "null":
            raise AuthenticationFailed(detail=_("No token provided."))

        return token

    def can_skip(self, request) -> bool:
        path = request.get_full_path()
        if path == "/":
            return True
        return path.split("/")[2] in ["docs", "swagger", "schema"]

    def is_logout(self, request) -> bool:
        logout_path = request.get_full_path()
        return "logout" in logout_path

    def authenticate(self, request):
        if self.can_skip(request):
            return (AnonymousUser(), None)

        is_logout_request = self.is_logout(request)
        raw_token = self.get_raw_token(request)
        token = CustomAccessToken(raw_token)
        
        token.check_blacklist()
        user = self.get_user_new(token)

        if not user.is_active:
            raise ValidationError(detail="user_blocked")

        return (user, None)
