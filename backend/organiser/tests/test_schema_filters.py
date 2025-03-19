from django.db.models import QuerySet
from django.test import TestCase
from django.db.models.signals import post_save

from organiser.models import Item, Project, ItemTypeOption, ItemStatusOption, ItemPriorityOption
from organiser.schema.filters import filter_items, filter_projects
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


class FilterProjectTest(TestCase):

    def test_filter_projects_name_contains_filter(self):
        """Test that the `name_contains` filter returns the expected filtered projects."""
        # Create some test data
        project_1 = Project.objects.create(name="Project 1")
        project_2 = Project.objects.create(name="project 2")  # lowercase
        project_3 = Project.objects.create(name="Project 3")
        # Create some test cases
        test_cases = [
            # name_contains, expected_queryset_as_list, description
            ("Project 2", [project_2], "A valid name should find 1 project"),
            ("ECT 2", [project_2], "A valid case-insensitive sub-string should find 1 project"),
            (
                "project",
                [project_1, project_2, project_3],
                "A common case-insensitive sub-string should return all projects",
            ),
            ("NOT FOUND", [], "A valid string but not in the set should find 0 projects"),
            (str, [], "An invalid type should, in effect, find 0 projects"),
            (None, [project_1, project_2, project_3], "None should skip the filter and return all projects"),
            ("", [project_1, project_2, project_3], "An empty string should skip the filter and return all projects"),
        ]
        # Run each test case
        for name_contains, expected_queryset_as_list, description in test_cases:
            all_projects = Project.objects.all()
            filtered_projects = filter_projects(all_projects, name_contains=name_contains)
            self.assertIsInstance(filtered_projects, QuerySet, description)
            self.assertEqual(list(filtered_projects), expected_queryset_as_list, description)


class FilterItemTest(TestCase):

    def setUp(self):
        post_save.disconnect(create_default_project_settings, sender=Project)
        _create_example_hierarchy(self)

    def tearDown(self):
        post_save.connect(create_default_project_settings, sender=Project)

    def test_filter_items_name_contains_filter(self):
        """Test that the `name_contains` filter returns the expected filtered items."""
        # Create some test cases
        test_cases = [
            # name_contains, expected_queryset_as_list, description
            ("Item 1 1 3 1", [self.item_1_1_3_1], "A valid name should find 1 item"),
            ("EM 1 1 3 1", [self.item_1_1_3_1], "A valid case-insensitive sub-string should find 1 item"),
            (
                "ITEM 1 1 3",
                [self.item_1_1_3, self.item_1_1_3_1],
                "A common case-insensitive sub-string should return multiple items",
            ),
            ("NOT FOUND", [], "A valid string but not in the set should find 0 items"),
            (str, [], "An invalid object should, in effect, find 0 items"),
            (None, list(Item.objects.all()), "None should skip the filter and return all items"),
            ("", list(Item.objects.all()), "An empty string should skip the filter and return all items"),
        ]
        # Run each test case
        for name_contains, expected_queryset_as_list, description in test_cases:
            all_items = Item.objects.all()
            filtered_items = filter_items(all_items, name_contains=name_contains)
            self.assertIsInstance(filtered_items, QuerySet, description)
            self.assertEqual(list(filtered_items), expected_queryset_as_list, description)

    def test_filter_items_project_filter(self):
        """Test that the `project` filter returns the expected filtered items."""
        # Create some test cases
        test_cases = [
            # project, expected_queryset_as_list, description
            (int(self.project_2.id), [self.item_2_1], "A valid project id value should find 1 item"),
            (self.project_2, [self.item_2_1], "A valid project instance should find 1 item"),
            (9999, [], "An invalid project id value should find 0 items"),
            # (self.item_1_1, [], "An invalid (not a) project instance should find 0 items"), # TODO
            (None, list(Item.objects.all()), "None should skip the filter and return all items"),
        ]
        # Run each test case
        for project, expected_queryset_as_list, description in test_cases:
            all_items = Item.objects.all()
            filtered_items = filter_items(all_items, project=project)
            self.assertIsInstance(filtered_items, QuerySet, description)
            self.assertEqual(list(filtered_items), expected_queryset_as_list, description)

    def test_filter_items_item_type_filter(self):
        """Test that the `item_type` filter returns the expected filtered items."""
        # Create some test cases
        test_cases = [
            # item_type, expected_queryset_as_list, description
            (int(self.project_1_item_type_feature.id), [self.item_1_1_1], "A valid choice value should find 1 item"),
            (self.project_1_item_type_feature, [self.item_1_1_1], "A valid choice member should find 1 item"),
            # TODO: an invalid member uses the value of that member (ie, ItemStatusOptionChoice)
            (999, [], "An invalid choice value should find 0 items"),
            (None, list(Item.objects.all()), "None should skip the filter and return all items"),
        ]
        # Run each test case
        for item_type, expected_queryset_as_list, description in test_cases:
            all_items = Item.objects.all()
            filtered_items = filter_items(all_items, item_type=item_type)
            self.assertIsInstance(filtered_items, QuerySet, description)
            self.assertEqual(list(filtered_items), expected_queryset_as_list, description)

    def test_filter_items_item_status_filter(self):
        """Test that the `item_status` filter returns the expected filtered items."""
        # Create some test cases
        test_cases = [
            # item_status, expected_queryset_as_list, description
            (
                int(self.project_1_item_status_in_progress.id),
                [self.item_1_2, self.item_1_1_2],
                "A valid choice value should find 2 items",
            ),
            (
                self.project_1_item_status_in_progress,
                [self.item_1_2, self.item_1_1_2],
                "A valid choice member should find 2 items",
            ),
            # TODO: an invalid member uses the value of that member (ie, ItemTypeOptionChoice)
            (999, [], "An invalid choice value should find 0 items"),
            (None, list(Item.objects.all()), "None should skip the filter and return all items"),
        ]
        # Run each test case
        for item_status, expected_queryset_as_list, description in test_cases:
            all_items = Item.objects.all()
            filtered_items = filter_items(all_items, item_status=item_status)
            self.assertIsInstance(filtered_items, QuerySet, description)
            self.assertEqual(list(filtered_items), expected_queryset_as_list, description)

    def test_filter_items_all_fields_filter(self):
        """Test that using all the filter returns the expected filtered items."""
        all_items = Item.objects.all()
        filtered_items = filter_items(
            all_items,
            name_contains="3 1",
            project=self.project_1,
            item_type=self.project_1_item_type_task,
            item_status=self.project_1_item_status_done,
            item_priority=self.project_1_item_priority_medium,
        )
        self.assertIsInstance(filtered_items, QuerySet)
        self.assertEqual(list(filtered_items), [self.item_1_1_3_1])
