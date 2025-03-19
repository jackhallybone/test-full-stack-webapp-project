import inspect

from django.contrib.auth import get_user_model
from graphql_jwt.testcases import JSONWebTokenTestCase
from organiser.models import Item, Project
from organiser.schema.types import ItemType, ProjectType


class ProjectTypeTest(JSONWebTokenTestCase):
    """We don't test defaults (fields, types), and the filtering logic is tested elsewhere."""

    def setUp(self):
        self.user = get_user_model().objects.create(username="test")
        self.project = Project.objects.create(name="project")

    def test_project_default_item_type_authenticated(self):
        """Test the default item type project related query, providing authentication for the original project query."""
        query = """
            query ProjectDescendants($id: ID!) {
                project (id: $id) {
                    defaultItemType {
                        name
                    }
                }
            }
        """
        variables = {"id": self.project.id}
        self.client.authenticate(self.user)
        response = self.client.execute(query, variables=variables)
        self.assertIsNone(response.errors, "An authenticated query should not return any errors.")
        self.assertEqual(
            response.data["project"]['defaultItemType']["name"],
            self.project.get_default_item_type().name
        )

    def test_project_default_item_status_authenticated(self):
        """Test the default item status project related query, providing authentication for the original project query."""
        query = """
            query ProjectDescendants($id: ID!) {
                project (id: $id) {
                    defaultItemStatus {
                        name
                    }
                }
            }
        """
        variables = {"id": self.project.id}
        self.client.authenticate(self.user)
        response = self.client.execute(query, variables=variables)
        self.assertIsNone(response.errors, "An authenticated query should not return any errors.")
        self.assertEqual(
            response.data["project"]['defaultItemStatus']["name"],
            self.project.get_default_item_status().name
        )

    def test_project_default_item_priority_authenticated(self):
        """Test the default item priority project related query, providing authentication for the original project query."""
        query = """
            query ProjectDescendants($id: ID!) {
                project (id: $id) {
                    defaultItemPriority {
                        name
                    }
                }
            }
        """
        variables = {"id": self.project.id}
        self.client.authenticate(self.user)
        response = self.client.execute(query, variables=variables)
        self.assertIsNone(response.errors, "An authenticated query should not return any errors.")
        self.assertEqual(
            response.data["project"]['defaultItemPriority']["name"],
            self.project.get_default_item_priority().name
        )

    def test_project_descendants_fields_match_resolver_args(self):
        """Test that the fields in the `descendants` definition match the args in the resolver."""
        definition_field_names = list(ProjectType._meta.fields["descendants"].args.keys())
        resolver_arg_names = list(inspect.signature(ProjectType.resolve_descendants).parameters.keys())
        resolver_arg_names.remove("self")
        resolver_arg_names.remove("info")
        self.assertEqual(definition_field_names, resolver_arg_names)

    def test_project_descendants_authenticated(self):
        """Test the descendants project related query, providing authentication for the original project query."""
        query = """
            query ProjectDescendants($id: ID!) {
                project (id: $id) {
                    descendants {
                        name
                    }
                }
            }
        """
        variables = {"id": self.project.id}
        self.client.authenticate(self.user)
        response = self.client.execute(query, variables=variables)
        self.assertIsNone(response.errors, "An authenticated query should not return any errors.")
        self.assertIsNotNone(response.data.get("project"), "An authenticated query should populate the project object.")
        self.assertIsNotNone(
            response.data["project"].get("descendants"), "An authenticated query should populate the descendants field."
        )

    def test_project_items_fields_match_resolver_args(self):
        """Test that the fields in the `items` definition match the args in the resolver."""
        definition_field_names = list(ProjectType._meta.fields["items"].args.keys())
        resolver_arg_names = list(inspect.signature(ProjectType.resolve_items).parameters.keys())
        resolver_arg_names.remove("self")
        resolver_arg_names.remove("info")
        self.assertEqual(definition_field_names, resolver_arg_names)

    def test_project_items_authenticated(self):
        """Test the items project related query, providing authentication for the original project query."""
        query = """
            query ProjectItems($id: ID!) {
                project (id: $id) {
                    items {
                        name
                    }
                }
            }
        """
        variables = {"id": self.project.id}
        self.client.authenticate(self.user)
        response = self.client.execute(query, variables=variables)
        self.assertIsNone(response.errors, "An authenticated query should not return any errors.")
        self.assertIsNotNone(response.data.get("project"), "An authenticated query should populate the project object.")
        self.assertIsNotNone(
            response.data["project"].get("items"), "An authenticated query should populate the items field."
        )

    def test_project_children_fields_match_resolver_args(self):
        """Test that the fields in the `children` definition match the args in the resolver."""
        definition_field_names = list(ProjectType._meta.fields["children"].args.keys())
        resolver_arg_names = list(inspect.signature(ProjectType.resolve_children).parameters.keys())
        resolver_arg_names.remove("self")
        resolver_arg_names.remove("info")
        self.assertEqual(definition_field_names, resolver_arg_names)

    def test_project_children_authenticated(self):
        """Test the children project related query, providing authentication for the original project query."""
        query = """
            query ProjectChildren($id: ID!) {
                project (id: $id) {
                    children {
                        name
                    }
                }
            }
        """
        variables = {"id": self.project.id}
        self.client.authenticate(self.user)
        response = self.client.execute(query, variables=variables)
        self.assertIsNone(response.errors, "An authenticated query should not return any errors.")
        self.assertIsNotNone(response.data.get("project"), "An authenticated query should populate the project object.")
        self.assertIsNotNone(
            response.data["project"].get("children"), "An authenticated query should populate the children field."
        )

    def test_project_num_children_authenticated(self):
        """Test the num_children project related query, providing authentication for the original project query."""
        query = """
            query ProjectNumChildren($id: ID!) {
                project (id: $id) {
                    numChildren
                }
            }
        """
        variables = {"id": self.project.id}
        self.client.authenticate(self.user)
        response = self.client.execute(query, variables=variables)
        self.assertIsNone(response.errors, "An authenticated query should not return any errors.")
        self.assertIsNotNone(response.data.get("project"), "An authenticated query should populate the project object.")
        self.assertIsNotNone(
            response.data["project"].get("numChildren"), "An authenticated query should populate the numChildren field."
        )


class ItemTypeTest(JSONWebTokenTestCase):
    """We don't test defaults (fields, types), and the filtering logic is tested elsewhere."""

    def setUp(self):
        self.user = get_user_model().objects.create(username="test")
        self.project = Project.objects.create(name="project")
        self.item = Item.objects.create(
            name="item",
            project=self.project,
            item_type=self.project.get_default_item_type(),
            item_status=self.project.get_default_item_status(),
            item_priority=self.project.get_default_item_priority(),
        )

    def test_item_ancestors_fields_match_resolver_args(self):
        """Test that the fields in the `ancestors` definition match the args in the resolver."""
        definition_field_names = list(ItemType._meta.fields["ancestors"].args.keys())
        resolver_arg_names = list(inspect.signature(ItemType.resolve_ancestors).parameters.keys())
        resolver_arg_names.remove("self")
        resolver_arg_names.remove("info")
        self.assertEqual(definition_field_names, resolver_arg_names)

    def test_item_ancestors_authenticated(self):
        """Test the ancestors item related query, providing authentication for the original item query."""
        query = """
            query ItemAncestors($id: ID!) {
                item (id: $id) {
                    ancestors {
                        name
                    }
                }
            }
        """
        variables = {"id": self.item.id}
        self.client.authenticate(self.user)
        response = self.client.execute(query, variables=variables)
        self.assertIsNone(response.errors, "An authenticated query should not return any errors.")
        self.assertIsNotNone(response.data.get("item"), "An authenticated query should populate the item object.")
        self.assertIsNotNone(
            response.data["item"].get("ancestors"), "An authenticated query should populate the ancestors field."
        )

    def test_item_descendants_fields_match_resolver_args(self):
        """Test that the fields in the `descendants` definition match the args in the resolver."""
        definition_field_names = list(ItemType._meta.fields["descendants"].args.keys())
        resolver_arg_names = list(inspect.signature(ItemType.resolve_descendants).parameters.keys())
        resolver_arg_names.remove("self")
        resolver_arg_names.remove("info")
        self.assertEqual(definition_field_names, resolver_arg_names)

    def test_item_descendants_authenticated(self):
        """Test the descendants item related query, providing authentication for the original item query."""
        query = """
            query ItemDescendants($id: ID!) {
                item (id: $id) {
                    descendants {
                        name
                    }
                }
            }
        """
        variables = {"id": self.item.id}
        self.client.authenticate(self.user)
        response = self.client.execute(query, variables=variables)
        self.assertIsNone(response.errors, "An authenticated query should not return any errors.")
        self.assertIsNotNone(response.data.get("item"), "An authenticated query should populate the item object.")
        self.assertIsNotNone(
            response.data["item"].get("descendants"), "An authenticated query should populate the descendants field."
        )

    def test_item_children_fields_match_resolver_args(self):
        """Test that the fields in the `children` definition match the args in the resolver."""
        definition_field_names = list(ItemType._meta.fields["children"].args.keys())
        resolver_arg_names = list(inspect.signature(ItemType.resolve_children).parameters.keys())
        resolver_arg_names.remove("self")
        resolver_arg_names.remove("info")
        self.assertEqual(definition_field_names, resolver_arg_names)

    def test_item_children_authenticated(self):
        """Test the children item related query, providing authentication for the original item query."""
        query = """
            query ItemChildren($id: ID!) {
                item (id: $id) {
                    children {
                        name
                    }
                }
            }
        """
        variables = {"id": self.item.id}
        self.client.authenticate(self.user)
        response = self.client.execute(query, variables=variables)
        self.assertIsNone(response.errors, "An authenticated query should not return any errors.")
        self.assertIsNotNone(response.data.get("item"), "An authenticated query should populate the item object.")
        self.assertIsNotNone(
            response.data["item"].get("children"), "An authenticated query should populate the children field."
        )

    def test_item_num_children_authenticated(self):
        """Test the num_children item related query, providing authentication for the original item query."""
        query = """
            query ItemNumChildren($id: ID!) {
                item (id: $id) {
                    numChildren
                }
            }
        """
        variables = {"id": self.item.id}
        self.client.authenticate(self.user)
        response = self.client.execute(query, variables=variables)
        self.assertIsNone(response.errors, "An authenticated query should not return any errors.")
        self.assertIsNotNone(response.data.get("item"), "An authenticated query should populate the item object.")
        self.assertIsNotNone(
            response.data["item"].get("numChildren"), "An authenticated query should populate the numChildren field."
        )
