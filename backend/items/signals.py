from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ItemLocation, ItemStatus, ItemType, Project


@receiver(post_save, sender=Project)
def create_default_item_attributes(sender, instance, created, **kwargs):
    """Create a set of default item options when a new project is created."""
    if created:
        for item_type in ItemType.default_options():
            ItemType.objects.create(project=instance, **item_type)
        for item_status in ItemStatus.default_options():
            ItemStatus.objects.create(project=instance, **item_status)
        for item_priority in ItemLocation.default_options():
            ItemLocation.objects.create(project=instance, **item_priority)
