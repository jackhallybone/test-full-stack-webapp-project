from django.core.exceptions import ValidationError
from django.db.models.signals import post_save

from django.test import TestCase
from organiser.models import Item, Project, ItemTypeOption, ItemStatusOption, ItemPriorityOption
from organiser.signals import create_default_project_settings

def _create_example_hierarchy(self):
    """Set up a basic hierarchy.
    - project_1
        - item_1_1 (area, to do, medium)
            - item_1_1_1 (feature, to do, high)
            - item_1_1_2 (task, in progress, medium)
            - item_1_1_3 (task, done, low)
                - item_1_1_3_1 (task, done, medium)
        - item_1_2 (epic, in progress, low)
    - project_2
        -item_2_1 (task, to do, medium)
    """
    # Create a project
    self.project_1 = Project.objects.create(name="Project 1")

    # Explicitly define the item options, rather than relying on the default options
    self.project_1_item_type_area = ItemTypeOption.objects.create(project=self.project_1, name="Area", order=1, nestable=False, default=False)
    self.project_1_item_type_epic = ItemTypeOption.objects.create(project=self.project_1, name="Epic", order=2, nestable=False, default=False)
    self.project_1_item_type_feature = ItemTypeOption.objects.create(project=self.project_1, name="Feature", order=3, nestable=False, default=False)
    self.project_1_item_type_task = ItemTypeOption.objects.create(project=self.project_1, name="Task", order=4, nestable=True, default=True)
    self.project_1_item_status_to_do = ItemStatusOption.objects.create(project=self.project_1, name="To Do", order=1, default=True)
    self.project_1_item_status_in_progress = ItemStatusOption.objects.create(project=self.project_1, name="In Progress", order=2, default=False)
    self.project_1_item_status_done = ItemStatusOption.objects.create(project=self.project_1, name="Done", order=3, default=False)
    self.project_1_item_priority_high = ItemPriorityOption.objects.create(project=self.project_1, name="High", order=1, default=False)
    self.project_1_item_priority_medium = ItemPriorityOption.objects.create(project=self.project_1, name="Medium", order=2, default=True)
    self.project_1_item_priority_low = ItemPriorityOption.objects.create(project=self.project_1, name="Low", order=3, default=False)

    # Create the item hierarchy
    self.item_1_1 = Item.objects.create(
        name="Item 1 1",
        project=self.project_1,
        item_type=self.project_1_item_type_area,
        item_status=self.project_1_item_status_to_do,
        item_priority=self.project_1_item_priority_medium,
    )
    self.item_1_1_1 = Item.objects.create(
        name="Item 1 1 1",
        project=self.project_1,
        parent=self.item_1_1,
        item_type=self.project_1_item_type_feature,
        item_status=self.project_1_item_status_to_do,
        item_priority=self.project_1_item_priority_high,
    )
    self.item_1_1_2 = Item.objects.create(
        name="Item 1 1 2",
        project=self.project_1,
        parent=self.item_1_1,
        item_type=self.project_1_item_type_task,
        item_status=self.project_1_item_status_in_progress,
        item_priority=self.project_1_item_priority_medium,
    )
    self.item_1_1_3 = Item.objects.create(
        name="Item 1 1 3",
        project=self.project_1,
        parent=self.item_1_1,
        item_type=self.project_1_item_type_task,
        item_status=self.project_1_item_status_done,
        item_priority=self.project_1_item_priority_low,
    )
    self.item_1_1_3_1 = Item.objects.create(
        name="Item 1 1 3 1",
        project=self.project_1,
        parent=self.item_1_1_3,
        item_type=self.project_1_item_type_task,
        item_status=self.project_1_item_status_done,
        item_priority=self.project_1_item_priority_medium,
    )
    self.item_1_2 = Item.objects.create(
        name="Item 1 2",
        project=self.project_1,
        item_type=self.project_1_item_type_epic,
        item_status=self.project_1_item_status_in_progress,
        item_priority=self.project_1_item_priority_low,
    )

    # Create a second project outside the other hierarchy
    self.project_2 = Project.objects.create(name="Project 2")
    self.project_2_item_type_task = ItemTypeOption.objects.create(project=self.project_2, name="Task", order=4, nestable=True, default=True)
    self.project_2_item_status_to_do = ItemStatusOption.objects.create(project=self.project_2, name="To Do", order=1, default=True)
    self.project_2_item_priority_medium = ItemPriorityOption.objects.create(project=self.project_2, name="Medium", order=2, default=True)
    self.item_2_1 = Item.objects.create(
        name="Item 2 1",
        project=self.project_2,
        item_type=self.project_2_item_type_task,
        item_status=self.project_2_item_status_to_do,
        item_priority=self.project_2_item_priority_medium,
    )


class ProjectModelTest(TestCase):
    def setUp(self):
        post_save.disconnect(create_default_project_settings, sender=Project)
        _create_example_hierarchy(self)

    def tearDown(self):
        post_save.connect(create_default_project_settings, sender=Project)

    def test_project_ordering(self):
        """Test the ordering of projects when listed."""
        self.assertEqual(list(Project.objects.all()), [self.project_1, self.project_2])

    def test_project_str(self):
        """Test the string representation of the project model."""
        self.assertEqual(str(self.project_1), "Project 1")

    def test_project_get_default_item_type(self):
        """Test that the project can retrieve the item type option set to default."""
        self.assertEqual(
            self.project_1.get_default_item_type(),
            self.project_1_item_type_task
        )

    def test_project_get_default_item_status(self):
        """Test that the project can retrieve the item status option set to default."""
        self.assertEqual(
            self.project_1.get_default_item_status(),
            self.project_1_item_status_to_do
        )

    def test_project_get_default_item_priority(self):
        """Test that the project can retrieve the item priority option set to default."""
        self.assertEqual(
            self.project_1.get_default_item_priority(),
            self.project_1_item_priority_medium
        )

    def test_project_descendants(self):
        """Test the `project.get_descendants()` method (see `ItemModelTest.test_project_ordering()`)."""
        self.assertEqual(
            list(self.project_1.get_descendants()),
            [self.item_1_1, self.item_1_2, self.item_1_1_1, self.item_1_1_2, self.item_1_1_3, self.item_1_1_3_1],
        )

    def test_project_children(self):
        """Test the `project.get_children()` method."""
        self.assertEqual(list(self.project_1.get_children()), [self.item_1_1, self.item_1_2])

    def test_item_num_children(self):
        """Test the `project.get_num_children()` method."""
        self.assertEqual(self.project_1.get_num_children(), 2)

    def test_project_strip_name(self):
        """Test that leading and trailing whitespace is removed from the name."""
        self.project_1.name = "  a name with whitespace   "
        self.project_1.clean()
        self.assertEqual(self.project_1.name, "a name with whitespace")

    def test_project_prevent_empty_name(self):
        """Test that empty names are rejected."""
        self.project_1.name = ""  # empty name
        with self.assertRaises(ValidationError):
            self.project_1.save()


class ProjectOptionsTest(TestCase):
    """Testing the abstract class using the ItemTypeOption which extends it."""
    def setUp(self):
        post_save.disconnect(create_default_project_settings, sender=Project)
        self.project = Project.objects.create(name="Project")
        self.item_type = ItemTypeOption.objects.create(project=self.project, name="Task", order=1, nestable=True, default=True)

    def tearDown(self):
        post_save.connect(create_default_project_settings, sender=Project)

    def test_project_option_str(self):
        """Test the string representation of the project options model."""
        self.assertEqual(str(self.item_type), "Project: Task")

    def test_project_option_unique_name(self):
        """Test that the validation does not allow a project to have options with the same name."""
        with self.assertRaises(ValidationError):
            ItemTypeOption.objects.create(project=self.project, name="Task", order=2, nestable=False, default=False)

    def test_project_option_unique_order(self):
        """Test that the validation does not allow a project to have options with the same order."""
        with self.assertRaises(ValidationError):
            ItemTypeOption.objects.create(project=self.project, name="Area", order=1, nestable=False, default=False)

    def test_project_option_only_one_default(self):
        """Test that the validation does not allow a project to have more than one default option."""
        with self.assertRaises(ValidationError):
            ItemTypeOption.objects.create(project=self.project, name="Area", order=2, nestable=False, default=True)


class ItemModelTest(TestCase):
    def setUp(self):
        post_save.disconnect(create_default_project_settings, sender=Project)
        _create_example_hierarchy(self)

    def tearDown(self):
        post_save.connect(create_default_project_settings, sender=Project)

    def test_item_invalid_project_type(self):
        """Test that invalid project types are rejected."""
        with self.assertRaises(ValueError):
            self.item_1_1.project = 1

    def test_item_invalid_project_object(self):
        """Test that invalid project objects (eg, not saved) are rejected."""
        item = Item(
            name="Unsaved Item",
            project=Project(name="Unsaved Project"),
            item_type=self.project_2_item_type_task,
            item_status=self.project_2_item_status_to_do,
            item_priority=self.project_2_item_priority_medium,
        )
        with self.assertRaises(ValueError):
            item.save()

    def test_item_invalid_parent_type(self):
        """Test that invalid parent types are rejected."""
        with self.assertRaises(ValueError):
            self.item_1_1.parent = 1

    def test_item_invalid_parent_object(self):
        """Test that invalid parent objects (eg, not saved) are rejected."""
        self.item_2_1.parent = Item(
            name="Unsaved Item",
            project=self.project_2,
            item_type=self.project_2_item_type_task,
            item_status=self.project_2_item_status_to_do,
            item_priority=self.project_2_item_priority_medium,
        )
        with self.assertRaises(ValueError):
            self.item_2_1.save()

    def test_item_ordering(self):
        """Test the ordering of items when listed."""
        self.assertEqual(
            list(Item.objects.all()),
            [
                self.item_1_1,
                self.item_1_2,
                self.item_1_1_1,
                self.item_1_1_2,
                self.item_1_1_3,
                self.item_1_1_3_1,
                self.item_2_1,
            ],
        )

    def test_item_str(self):
        """Test the string representation of the item model."""
        self.assertEqual(str(self.item_1_1), "Area: Item 1 1")

    def test_item_ancestors(self):
        """Test the `item.get_ancestors()` method."""
        self.assertEqual(list(self.item_1_1_3_1.get_ancestors()), [self.item_1_1, self.item_1_1_3])

    def test_item_descendants(self):
        """Test the `item.get_descendants()` method (see `ItemModelTest.test_project_ordering()`)."""
        self.assertEqual(
            list(self.item_1_1.get_descendants()),
            [self.item_1_1_1, self.item_1_1_2, self.item_1_1_3, self.item_1_1_3_1],
        )

    def test_item_children(self):
        """Test the `item.get_children()` method (see `ItemModelTest.test_project_ordering()`)."""
        self.assertEqual(list(self.item_1_1.get_children()), [self.item_1_1_1, self.item_1_1_2, self.item_1_1_3])

    def test_item_num_children(self):
        """Test the `item.get_num_children()` method."""
        self.assertEqual(self.item_1_1.get_num_children(), 3)

    def test_item_strip_name(self):
        """Test that leading and trailing whitespace is removed from the name."""
        self.item_1_1.name = "  a name with whitespace   "
        self.item_1_1.clean()
        self.assertEqual(self.item_1_1.name, "a name with whitespace")

    def test_item_prevent_empty_name(self):
        """Test that empty names are rejected."""
        self.item_1_1.name = ""  # empty name
        with self.assertRaises(ValidationError):
            self.item_1_1.save()

    def test_item_prevent_changing_project(self):
        """Test the validation which prevents an item changing project once created."""
        self.item_1_1.project = self.project_2
        with self.assertRaises(ValidationError):
            self.item_1_1.clean()

    def test_item_invalid_item_type(self):
        """Test that invalid item types are rejected."""
        with self.assertRaises(ValueError):
            self.item_1_1.item_type = 1

    def test_item_invalid_item_type_object(self):
        """Test that invalid item type objects (eg, not saved) are rejected."""
        self.item_1_1.item_type = ItemTypeOption(name="invalid type", project=self.project_1, order=999)
        with self.assertRaises(ValidationError):
            self.item_1_1.save()

    def test_item_invalid_item_status(self):
        """Test that invalid item statuses are rejected."""
        with self.assertRaises(ValueError):
            self.item_1_1.item_status = 1

    def test_item_invalid_item_status_object(self):
        """Test that invalid item status objects (eg, not saved) are rejected."""
        self.item_1_1.item_status = ItemStatusOption(name="invalid status", project=self.project_1, order=999)
        with self.assertRaises(ValidationError):
            self.item_1_1.save()

    def test_item_invalid_item_priority(self):
        """Test that invalid item priorities are rejected."""
        with self.assertRaises(ValueError):
            self.item_1_1.item_priority = 1

    def test_item_invalid_item_priority_object(self):
        """Test that invalid item priority objects (eg, not saved) are rejected."""
        self.item_1_1.item_priority = ItemPriorityOption(name="invalid priority", project=self.project_1, order=999)
        with self.assertRaises(ValidationError):
            self.item_1_1.save()

    def test_item_prevent_self_parenting(self):
        """Test the validation which prevents an item be its own parent."""
        self.item_1_1.parent = self.item_1_1  # self
        with self.assertRaises(ValidationError):
            self.item_1_1.clean()

    def test_item_prevent_crossing_projects(self):
        """Test the validation which prevents items from being assigned between projects."""
        self.item_1_1.parent = self.item_2_1  # in a different project
        with self.assertRaises(ValidationError):
            self.item_1_1.clean()

    def test_item_prevent_ancestor_circular_references(self):
        """Test the validation which prevents circular references in the hierarchy by checking ancestors."""
        self.item_1_1_3.parent = self.item_1_1_3_1  # create an item_1_1_3 > item_1_1_3_1 > item_1_1_3 loop
        with self.assertRaises(ValidationError):
            self.item_1_1_3.clean()

    def test_item_allow_nestable_item_types_to_nest(self):
        """Test the validation which allows nesting of the same item_types if they are nestable."""
        item = Item(
            name="Child Item",
            project=self.project_1,
            parent=self.item_1_1_3,  # which is also of type Task and tasks are nestable
            item_type=self.project_1_item_type_task,
            item_status=self.project_1_item_status_to_do,
            item_priority=self.project_1_item_priority_medium
        )
        # Task can nest under the same type Task because tasks are nestable
        item.save()

    def test_item_prevent_non_nestable_item_types_from_nesting(self):
        """Test the validation which prevents nesting of the same item_types if they are not nestable."""
        item = Item(
            name="Child Item",
            project=self.project_1,
            parent=self.item_1_1,  # which is also of type Area and areas are not nestable
            item_type=self.project_1_item_type_area,
            item_status=self.project_1_item_status_to_do,
            item_priority=self.project_1_item_priority_medium
        )
        # Area cannot nest under the same type Area because areas are not nestable
        with self.assertRaises(ValidationError):
            item.save()

    def test_item_prevent_incorrect_item_type_ordering(self):
        """Test the validation which prevents different item_types from nesting under lower types."""
        item = Item(
            name="Child Item",
            project=self.project_1,
            parent=self.item_1_1_1,  # which is of type Feature
            item_type=self.project_1_item_type_area,
            item_status=self.project_1_item_status_to_do,
            item_priority=self.project_1_item_priority_medium
        )
        # Area cannot nest under the different type Feature because Feature is below Area in the hierarchy
        with self.assertRaises(ValidationError):
            item.save()

    def test_item_unique_kanban_row_order(self):
        """Test that the validation does not allow a parent (or null parent) to have items with the same kanban row order value."""
        _ = Item.objects.create(
            name="Item 1",
            project=self.project_1,
            item_type=self.project_1_item_type_area,
            item_status=self.project_1_item_status_to_do,
            item_priority=self.project_1_item_priority_medium,
            kanban_row_order=1
        )
        with self.assertRaises(ValidationError):
            _ = Item.objects.create(
            name="Item 2",
            project=self.project_1,
            item_type=self.project_1_item_type_area,
            item_status=self.project_1_item_status_to_do,
            item_priority=self.project_1_item_priority_medium,
            kanban_row_order=1
        )

    def test_item_deletion_from_project(self):
        """Test the foreign key `Item.project.on_delete` propagation."""
        self.project_2.delete()
        self.assertFalse(Item.objects.filter(id=self.item_2_1.id).exists())
        self.assertTrue(Item.objects.filter(id=self.item_1_1.id).exists())  # not in project_2's hierarchy

    def test_item_deletion_from_parent(self):
        """Test the foreign key `Item.parent.on_delete` propagation."""
        self.item_1_1.delete()
        self.assertFalse(Item.objects.filter(id=self.item_1_1_1.id).exists())
        self.assertTrue(Item.objects.filter(id=self.item_1_2.id).exists())  # not in item_1_1's hierarchy

    def test_item_stress_test_hierarchy_depth_limit(self):
        """Test the stability of creating and fetching in a deeply nested hierarchy."""
        project = Project.objects.create(name="Project A")
        item_type_task = ItemTypeOption.objects.create(project=project, name="Task", order=4, nestable=True, default=True)
        item_status_to_do = ItemStatusOption.objects.create(project=project, name="To Do", order=1, default=True)
        item_priority_medium = ItemPriorityOption.objects.create(project=project, name="Medium", order=2, default=True)

        first_descendant = Item.objects.create(
            name="Parent",
            project=project,
            item_type=item_type_task,
            item_status=item_status_to_do,
            item_priority=item_priority_medium
        )

        # Create a nested hierarchy that is deeper than would reasonably be expected
        num_levels = 100
        parent = first_descendant
        for i in range(num_levels):
            latest_descendant = Item.objects.create(
                name=f"Child {i}",
                project=project,
                parent=parent,
                item_type=item_type_task,
                item_status=item_status_to_do,
                item_priority=item_priority_medium
            )
            parent = latest_descendant

        # Test the get_descendants function from the first descendant
        descendants = first_descendant.get_descendants()
        self.assertEqual(len(descendants), num_levels)

        # Test the get_ancestors function from the deepest descendant
        ancestors = latest_descendant.get_ancestors()
        self.assertEqual(len(ancestors), num_levels)

        # Project.get_descendants, Project.get_children and Item.get_children are relationships not custom getters
