from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from django.utils.translation import gettext_lazy as _

from .mixins import AuditMixin
from .models import Project, ItemTypeOption, ItemStatusOption, ItemPriorityOption


@receiver(pre_save)
def audit_fields(sender, instance, **kwargs):
    """Automatically sets `created_by` and `updated_by` fields on models inheriting from `AuditMixin` before saving."""
    if issubclass(sender, AuditMixin):
        request = getattr(instance, "_request", None)
        if request:
            if not instance.pk:
                instance.created_by = request.user
            instance.updated_by = request.user


@receiver(post_save, sender=Project)
def create_default_project_settings(sender, instance, created, **kwargs):
    if created:
        # Create default ItemTypes
        default_item_types = [
            {'name': _('Area'), 'order': 1, 'nestable': False, 'default': False},
            {'name': _('Epic'), 'order': 2, 'nestable': False, 'default': False},
            {'name': _('Feature'), 'order': 3, 'nestable': False, 'default': False},
            {'name': _('Task'), 'order': 4, 'nestable': True, 'default': True},
        ]
        for item_type in default_item_types:
            ItemTypeOption.objects.create(project=instance, **item_type)

        # Create default ItemStatuses
        default_item_statuses = [
            {'name': _('To Do'), 'order': 1, 'default': True},
            {'name': _('In Progress'), 'order': 2, 'default': False},
            {'name': _('Done'), 'order': 3, 'default': False},
        ]
        for item_status in default_item_statuses:
            ItemStatusOption.objects.create(project=instance, **item_status)

        # Create default ItemPriorities
        default_item_priorities = [
            {'name': _('High'), 'order': 1, 'default': False},
            {'name': _('Medium'), 'order': 2, 'default': True},
            {'name': _('Low'), 'order': 3, 'default': False},
        ]
        for item_priority in default_item_priorities:
            ItemPriorityOption.objects.create(project=instance, **item_priority)