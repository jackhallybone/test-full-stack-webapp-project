from django.test import TestCase
from django.contrib.auth import get_user_model
from organiser.models import Project, ItemTypeOption, ItemStatusOption, ItemPriorityOption


class ProjectSignalTests(TestCase):

    def setUp(self):
        """Create two users and some initial data."""
        self.user = get_user_model().objects.create_user(username="testuser", password="testpassword")
        self.user2 = get_user_model().objects.create_user(username="testuser2", password="testpassword2")
        self.project = Project(name="Test Project")
        # Save the project using the first user
        self.project._request = type('Request', (), {'user': self.user})
        self.project.save()  # This triggers the post_save signal

    def test_audit_fields_on_update(self):
        """Test that the 'created_by' and 'updated_by' fields are set correctly when a Project is updated."""
        # Simulate update by the second user
        self.project.name = "Updated Project"
        self.project._request = type('Request', (), {'user': self.user2})
        self.project.save()
        self.assertEqual(self.project.created_by, self.user)
        self.assertEqual(self.project.updated_by, self.user2)

    def test_project_with_correct_options_on_creation(self):
        """Test that the projects ItemTypeOptions, ItemStatusOptions, and ItemPriorityOptions have correct default data after project creation."""

        item_type_options = ItemTypeOption.objects.filter(project=self.project)
        self.assertEqual(item_type_options.count(), 4)
        self.assertTrue(item_type_options.filter(name='Area').exists())
        self.assertTrue(item_type_options.filter(name='Epic').exists())
        self.assertTrue(item_type_options.filter(name='Feature').exists())
        self.assertTrue(item_type_options.filter(name='Task').exists())

        item_status_options = ItemStatusOption.objects.filter(project=self.project)
        self.assertEqual(item_status_options.count(), 3)
        self.assertTrue(item_status_options.filter(name='To Do').exists())
        self.assertTrue(item_status_options.filter(name='In Progress').exists())
        self.assertTrue(item_status_options.filter(name='Done').exists())

        item_priority_options = ItemPriorityOption.objects.filter(project=self.project)
        self.assertEqual(item_priority_options.count(), 3)
        self.assertTrue(item_priority_options.filter(name='High').exists())
        self.assertTrue(item_priority_options.filter(name='Medium').exists())
        self.assertTrue(item_priority_options.filter(name='Low').exists())
