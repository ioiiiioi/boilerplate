import logging
import re
from django.db import IntegrityError
from django.http.request import QueryDict
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotAuthenticated
from rest_framework.generics import (
    CreateAPIView as CreateView,
    ListAPIView as ListView,
    RetrieveAPIView as RetrieveView,
    DestroyAPIView as DestroyView,
    UpdateAPIView as UpdateView,
)

logger = logging.getLogger(__name__)  # TODO: replace to struclog wait setup from Rede


# Regex to extract any key and its value | use for integrity db error
pattern = r"\(([^)]+)\)=\(([^)]+)\)"


def secure_query_dict(data: QueryDict):
    copy_data = data.copy()
    # check if data has password and pop it
    if copy_data.get("password"):
        copy_data.pop("password")
    return copy_data


# TODO: LoggingViewMixins is defined but never used - remove this class or use it in views
class LoggingViewMixins:

    def create(self, request, *args, **kwargs):
        """
        Create a model instance and add some logger.
        """
        print("<============== through logging mixins =========================>")
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as exc:
            data = secure_query_dict(request.data)
            logger.warning("Request Body: {data}".format(data={**data}))
            raise ValidationError(exc.detail)
        except NotAuthenticated as exc:
            data = secure_query_dict(request.data)
            logger.warning("Request Body: {data}".format(data={**data}))
            raise NotAuthenticated(exc.detail)

        try:
            self.perform_create(serializer)
        except IntegrityError as exc:
            # search key and value from error string
            match = re.search(pattern, exc.args[0])
            if match:
                key = match.group(1)
                value = match.group(2)
                logger.warning("Duplicate Data: {value}".format(value=value))
                raise ValidationError({key: ["Already exists."]})

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def destroy(self, request, *args, **kwargs):
        """
        Destroy a model instance and add some logger.
        """
        instance = self.get_object()
        id = instance.id
        self.perform_destroy(instance)
        logger.info("Deleted Data: {data}, {id}".format(data=instance, id=id))
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        """
        Update a model instance.
        """

        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as exc:
            data = secure_query_dict(request.data)
            logger.warning("Request Body: {data}".format(data={**data}))
            raise ValidationError(exc.detail)
        except NotAuthenticated as exc:
            data = secure_query_dict(request.data)
            logger.warning("Request Body: {data}".format(data={**data}))
            raise NotAuthenticated(exc.detail)

        try:
            self.perform_update(serializer)
        except IntegrityError as exc:
            # search key and value from error string
            match = re.search(pattern, exc.args[0])
            if match:
                key = match.group(1)
                value = match.group(2)
                logger.warning("Duplicate Data: {value}".format(value=value))
                raise ValidationError({key: ["Already exists."]})

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        logger.info("Updated Data: {data}".format(data=serializer.data))

        return Response(serializer.data)


class CreateAPIView(CreateView):
    """
    Concrete view for creating a model instance.
    """

    def create(self, request, *args, **kwargs):
        """
        Create a model instance and add some logger.
        """
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as exc:
            data = secure_query_dict(request.data)
            logger.warning("Request Body: {data}".format(data={**data}))
            raise ValidationError(exc.detail)
        except NotAuthenticated as exc:
            data = secure_query_dict(request.data)
            logger.warning("Request Body: {data}".format(data={**data}))
            raise NotAuthenticated(exc.detail)

        try:
            self.perform_create(serializer)
        except IntegrityError as exc:
            # search key and value from error string
            match = re.search(pattern, exc.args[0])
            if match:
                key = match.group(1)
                value = match.group(2)
                logger.warning("Duplicate Data: {value}".format(value=value))
                raise ValidationError({key: ["Already exists."]})

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ListAPIView(ListView):
    """
    Concrete view for listing a queryset.
    """

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class RetrieveAPIView(RetrieveView):
    """
    Concrete view for retrieving a model instance.
    """

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class DestroyAPIView(DestroyView):
    """
    Concrete view for deleting a model instance.
    """

    def destroy(self, request, *args, **kwargs):
        """
        Destroy a model instance and add some logger.
        """
        instance = self.get_object()
        id = instance.id
        self.perform_destroy(instance)
        logger.info("Deleted Data: {data}, {id}".format(data=instance, id=id))
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class UpdateAPIView(UpdateView):
    """
    Concrete view for updating a model instance.
    """

    def update(self, request, *args, **kwargs):
        """
        Update a model instance.
        """

        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as exc:
            data = secure_query_dict(request.data)
            logger.warning("Request Body: {data}".format(data={**data}))
            raise ValidationError(exc.detail)
        except NotAuthenticated as exc:
            data = secure_query_dict(request.data)
            logger.warning("Request Body: {data}".format(data={**data}))
            raise NotAuthenticated(exc.detail)

        try:
            self.perform_update(serializer)
        except IntegrityError as exc:
            # search key and value from error string
            match = re.search(pattern, exc.args[0])
            if match:
                key = match.group(1)
                value = match.group(2)
                logger.warning("Duplicate Data: {value}".format(value=value))
                raise ValidationError({key: ["Already exists."]})

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        logger.info("Updated Data: {data}".format(data=serializer.data))

        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ListCreateAPIView(ListAPIView, CreateAPIView):
    """
    Concrete view for listing a queryset or creating a model instance.
    """

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class RetrieveUpdateAPIView(RetrieveAPIView, UpdateAPIView):
    """
    Concrete view for retrieving, updating a model instance.
    """

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class RetrieveDestroyAPIView(RetrieveAPIView, DestroyAPIView):
    """
    Concrete view for retrieving or deleting a model instance.
    """

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class RetrieveUpdateDestroyAPIView(RetrieveUpdateAPIView, DestroyAPIView):
    """
    Concrete view for retrieving, updating or deleting a model instance.
    """

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
