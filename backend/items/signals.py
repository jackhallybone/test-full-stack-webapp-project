from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from .mixins import AuditMixin
from .models import ItemLocation, ItemStatus, ItemType, Project

# @receiver(pre_save)
# def audit_fields(sender, instance, **kwargs):
#     """Automatically sets `created_by` and `updated_by` fields on models inheriting from `AuditMixin` before saving."""
#     if issubclass(sender, AuditMixin):
#         request = getattr(instance, "_request", None)
#         if request:
#             if not instance.pk:
#                 instance.created_by = request.user
#             instance.updated_by = request.user


@receiver(post_save, sender=Project)
def create_default_project_settings(sender, instance, created, **kwargs):
    """Create a set of default item options when a new project is created."""
    if created:
        for item_type in ItemType.default_options():
            ItemType.objects.create(project=instance, **item_type)
        for item_status in ItemStatus.default_options():
            ItemStatus.objects.create(project=instance, **item_status)
        for item_priority in ItemLocation.default_options():
            ItemLocation.objects.create(project=instance, **item_priority)
