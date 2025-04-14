from django.db import models


class TimeStampedModels(models.Model):
    """
    Abstract base class that provides self-updating 'created' and 'modified' fields.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserCreatorModels(TimeStampedModels):
    """
    Abstract base class that provides a 'created_by' field.
    """
    created_by = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="%(class)s_created_by",
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True

