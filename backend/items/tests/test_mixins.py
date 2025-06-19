from django.test import TestCase
from django.utils import timezone

from items.models import Project


class AuditMixinTests(TestCase):

    def test_audit_mixin_timestamps(self):
        """Test that the created_at and updated_at fields are set and updated."""
        # Set
        project = Project.objects.create(name="project")
        self.assertIsInstance(project.created_at, timezone.datetime)
        self.assertIsInstance(project.updated_at, timezone.datetime)
        # Update
        original_created_at = project.created_at
        original_updated_at = project.updated_at
        project.name = "new name"
        project.save()
        self.assertEqual(project.created_at, original_created_at)
        self.assertNotEqual(project.updated_at, original_updated_at)
