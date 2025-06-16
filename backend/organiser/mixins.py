from django.conf import settings
from django.db import models


class AuditMixin(models.Model):
    """
    An abstract mixin model for tracking model creation and update metadata.

    Fields:
        # created_by (ForeignKey): The user who created the record. Auto-set with a pre-save signal. Nullable.
        created_at (datetime): The timestamp when the record was created. Auto-set on creation.
        # updated_by (ForeignKey): The user who last updated the record. Auto-set with a pre-save signal. Nullable.
        updated_at (datetime): The timestamp when the record was last updated. Auto-set on update.
    """

    # created_by = models.ForeignKey(
    #     settings.AUTH_USER_MODEL, related_name="created_%(class)s", on_delete=models.SET_NULL, null=True, blank=True
    # )
    created_at = models.DateTimeField(auto_now_add=True)
    # updated_by = models.ForeignKey(
    #     settings.AUTH_USER_MODEL, related_name="updated_%(class)s", on_delete=models.SET_NULL, null=True, blank=True
    # )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
