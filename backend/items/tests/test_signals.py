from django.test import TestCase

from items.models import ItemLocation, ItemStatus, ItemType, Project


class ProjectSignalTests(TestCase):

    def test_create_default_item_attributes(self):
        """Verify that the default project settings are created when a new project is created."""

        self.project = Project.objects.create(name="Test Project")

        item_types = ItemType.objects.filter(project=self.project)
        self.assertEqual(item_types.count(), len(ItemType.default_options()))

        item_statuses = ItemStatus.objects.filter(project=self.project)
        self.assertEqual(item_statuses.count(), len(ItemStatus.default_options()))

        item_locations = ItemLocation.objects.filter(project=self.project)
        self.assertEqual(item_locations.count(), len(ItemLocation.default_options()))
