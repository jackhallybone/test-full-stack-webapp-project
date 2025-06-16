from django.test import TestCase
from django.db.models.signals import post_save

from organiser.admin import ItemAdmin, ProjectAdmin
from organiser.models import Item, Project, ItemType, ItemStatus, ItemLocation
from organiser.signals import create_default_project_settings


class ProjectAdminTest(TestCase):

    def test_project_fieldset_fields_all_displayed(self):
        """Test that all project model fields are included on the admin change page."""
        model_fields = [field.name for field in Project._meta.fields]
        model_fields.remove("id")  # we don't expect id to be in the admin page
        admin_fields = [field for fieldset in ProjectAdmin.fieldsets for field in fieldset[1]["fields"]]
        self.assertEqual(sorted(model_fields), sorted(admin_fields))

    def test_project_descendants_count(self):
        """Test the counting and formatting of the descendants count in the project list view."""
        # Create a project with descendants
        project = Project.objects.create(name="project")
        _ = Item.objects.create(
            name="item 1",
            project=project,
            item_type=project.get_default_item_type(),
            item_status=project.get_default_item_status(),
            item_location=project.get_default_item_location(),
        )
        _ = Item.objects.create(
            name="item 2",
            project=project,
            item_type=project.get_default_item_type(),
            item_status=project.get_default_item_status(),
            item_location=project.get_default_item_location(),
        )
        # Create an instance of ProjectAdmin then call the descendants_count function
        project_admin = ProjectAdmin(model=Project, admin_site=None)
        descendants_count = project_admin.descendants_count(project)
        self.assertEqual(
            descendants_count,
            f'<a href="/admin/organiser/item/?project__id={project.id}">2</a>',
            "A project with descendants should show the number of descendants as an html link to the item view filtered for this project.",
        )


class ItemAdminTest(TestCase):

    def setUp(self):
        # Create a basic hierarchy
        post_save.disconnect(create_default_project_settings, sender=Project)
        self.project = Project.objects.create(name="project")
        self.item_type_task = ItemType.objects.create(project=self.project, name="Task", order=4, nestable=True, default=True)
        self.item_status_to_do = ItemStatus.objects.create(project=self.project, name="To Do", order=1, default=True)
        self.item_location_backlog = ItemLocation.objects.create(project=self.project, name="Backlog", order=1, default=True)
        self.item_1 = Item.objects.create(
            name="item 1",
            project=self.project,
            item_type=self.item_type_task,
            item_status=self.item_status_to_do,
            item_location=self.item_location_backlog,
        )
        self.item_2 = Item.objects.create(
            name="item 2",
            project=self.project,
            parent=self.item_1,
            item_type=self.item_type_task,
            item_status=self.item_status_to_do,
            item_location=self.item_location_backlog,
        )
        # Create an instance of ItemAdmin then call the ancestors_path function
        self.item_admin = ItemAdmin(model=Item, admin_site=None)

    def tearDown(self):
        post_save.connect(create_default_project_settings, sender=Project)

    def test_item_fieldset_fields_all_displayed(self):
        """Test that all item model fields are included on the admin change page."""
        model_fields = [field.name for field in Item._meta.fields]
        model_fields.remove("id")  # we don't expect id to be in the admin page
        admin_fields = [field for fieldset in ItemAdmin.fieldsets for field in fieldset[1]["fields"]]
        self.assertEqual(sorted(model_fields), sorted(admin_fields))

    def test_item_get_item_type_name(self):
        """Test that the field for item type can be populated with the name of the objects type."""
        item_type_name = self.item_admin.get_item_type_name(self.item_1)
        self.assertEqual(item_type_name, self.item_type_task.name)

    def test_item_get_item_status_name(self):
        """Test that the field for item status can be populated with the name of the objects status."""
        item_status_name = self.item_admin.get_item_status_name(self.item_1)
        self.assertEqual(item_status_name, self.item_status_to_do.name)

    def test_item_get_item_location_name(self):
        """Test that the field for item priority can be populated with the name of the objects priority."""
        item_location_name = self.item_admin.get_item_location_name(self.item_1)
        self.assertEqual(item_location_name, self.item_location_backlog.name)

    def test_item_option_formfield_for_foreignkey(self):
        """Test that the item option form field can get all the linked option objects."""
        def test(db_field_name, option_model):
            db_field = Item._meta.get_field(db_field_name)
            form_field_queryset = list(
                self.item_admin.formfield_for_foreignkey(db_field, request=None).queryset
            )
            all_options_queryset = list(option_model.objects.all())
            self.assertEqual(form_field_queryset, all_options_queryset)
        test("item_type", ItemType)
        test("item_status", ItemStatus)
        test("item_location", ItemLocation)

    def test_item_ancestors_path(self):
        """Test the formatting of the ancestors view in the item list view."""
        ancestors_path = self.item_admin.ancestors_path(self.item_2)
        self.assertEqual(
            ancestors_path,
            f'<a href="/admin/organiser/project/{self.project.id}/change/">{str(self.project)}</a> / <a href="/admin/organiser/item/{self.item_1.id}/change/">{str(self.item_1)}</a>',
            "An item with ancestors should show a linked breadcrumb of the ancestors, including it's project.",
        )

    def test_item_project_readonly_field(self):
        # For a new item, the obj argument will be None and project should not be readonly (be settable)
        readonly_fields = self.item_admin.get_readonly_fields(None, obj=None)
        self.assertNotIn("project", readonly_fields)
        # For an existing item, the obj argument will be the item and the project field should be readonly
        readonly_fields = self.item_admin.get_readonly_fields(None, obj=self.item_1)
        self.assertIn("project", readonly_fields)
