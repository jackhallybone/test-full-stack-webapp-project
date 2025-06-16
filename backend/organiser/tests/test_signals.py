from django.test import TestCase
from organiser.models import Project, ItemType, ItemStatus, ItemLocation


class ProjectSignalTests(TestCase):

    def test_create_default_project_settings(self):
        """Verify that the default project settings are created when a new project is created."""

        self.project = Project(name="Test Project")
        self.project.save()  # This triggers the post_save signal

        item_types = ItemType.objects.filter(project=self.project)
        self.assertEqual(item_types.count(), len(ItemType.default_options()))

        item_statuses = ItemStatus.objects.filter(project=self.project)
        self.assertEqual(item_statuses.count(), len(ItemStatus.default_options()))

        item_locations = ItemLocation.objects.filter(project=self.project)
        self.assertEqual(item_locations.count(), len(ItemLocation.default_options()))
