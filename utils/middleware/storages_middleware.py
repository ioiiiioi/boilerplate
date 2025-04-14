# from django.conf import settings as django_settings
# from django.utils.deconstruct import deconstructible
# from storages.backends.s3boto3 import S3Boto3Storage


# class CustomizedStorages(S3Boto3Storage):
#     def get_default_settings(self):
#         settings = super().get_default_settings()
#         settings["bucket_name"] = self._bucket
#         settings["location"] = self.location
#         return settings

#     def url(self, name, parameters=None, expire=None, http_method=None):
#         quickfix_url = f"https://{self.bucket.name}.s3.{django_settings.AWS_S3_REGION_NAME}.amazonaws.com/{self.location}{name}"
#         return quickfix_url


# @deconstructible
# class CustomizedStaticStorages(CustomizedStorages):
#     _bucket = django_settings.AWS_STATIC_BUCKET_NAME
#     location = "static/"


# @deconstructible
# class PublicMediaStorage(CustomizedStorages):
#     _bucket = django_settings.AWS_STATIC_BUCKET_NAME
#     location = "media/"


# @deconstructible
# class PrivateMediaStorage(S3Boto3Storage):
#     location = "media"
#     endpoint_url = f"https://{django_settings.AWS_STORAGE_BUCKET_NAME}.s3.{django_settings.AWS_S3_REGION_NAME}.amazonaws.com"

#     def get_default_settings(self):
#         settings = super().get_default_settings()
#         # to get presign url s3, force false `custom_domain`
#         settings["custom_domain"] = False
#         return settings
