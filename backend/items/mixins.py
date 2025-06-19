# from django.conf import settings
from django.db import models


class AuditMixin(models.Model):
    """An abstract mixin model for tracking model creation and update metadata.

    Attributes:
        created_at (datetime): The timestamp of when the object was created.
        updated_at (datetime): The timestamp of when the object was last updated.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
