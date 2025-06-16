from unittest.mock import Mock

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from organiser.models import Project


# class AuditMixinTests(TestCase):
#     # NOTE: we use the Project model which we know uses the AuditMixin and is in the database

#     def setUp(self):
#         self.user = get_user_model().objects.create_user(username="testuser", password="testpassword")
#         self.mock_request = Mock()
#         self.mock_request.user = self.user

#     def test_audit_mixin_created_by_and_created_at(self):
#         """Test that the created_by and created_at fields are set correctly."""
#         project = Project(name="project")
#         project._request = self.mock_request
#         project.save()
#         self.assertEqual(project.created_by, self.user)
#         self.assertIsInstance(project.created_at, timezone.datetime)

#     def test_audit_mixin_updated_by_and_updated_at(self):
#         """Test that updated_by and updated_at are set on model updates."""
#         project = Project(name="original")
#         project._request = self.mock_request
#         project.save()
#         original_updated_at = project.updated_at
#         # Make an update to the instance
#         project.name = "updated"
#         project._request = self.mock_request
#         project.save()
#         # Check that the updated_by field is set and updated_at has changed
#         self.assertEqual(project.updated_by, self.user)
#         self.assertIsInstance(project.updated_at, timezone.datetime)
#         self.assertNotEqual(project.updated_at, project.created_at)
#         self.assertNotEqual(project.updated_at, original_updated_at)
