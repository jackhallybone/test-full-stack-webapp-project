import inspect

import graphene
from django.contrib.auth import get_user_model
from graphql_jwt.testcases import JSONWebTokenTestCase
from organiser.models import Item, Project
from organiser.schema.queries import Query


class QueryTest(JSONWebTokenTestCase):

    def test_schema(self):
        """Check that the schema builds."""
        schema = graphene.Schema(query=Query)
        self.assertIsNotNone(schema)


class ProjectsQueryTest(JSONWebTokenTestCase):

    def setUp(self):
        """Create a user and some data to fetch for authentication testing."""
        self.user = get_user_model().objects.create(username="test")
        self.query = """
            query Projects {
                projects {
                    id
                }
            }
        """
        self.variables = {}

    def test_projects_fields_match_resolver_args(self):
        """Test that the fields in the `projects` definition match the args in the resolver."""
        definition_field_names = list(Query._meta.fields["projects"].args.keys())
        resolver_arg_names = list(inspect.signature(Query.resolve_projects).parameters.keys())
        resolver_arg_names.remove("self")
        resolver_arg_names.remove("info")
        self.assertEqual(definition_field_names, resolver_arg_names)

    def test_projects_authenticated(self):
        """Verify that the projects query accessible when the query is authenticated."""
        self.client.authenticate(self.user)
        response = self.client.execute(self.query, variables=self.variables)
        self.assertIsNone(response.errors, "An authenticated query should not return any errors.")
        self.assertIsNotNone(
            response.data.get("projects"), "An authenticated query should populate the projects object."
        )

    def test_projects_not_authenticated(self):
        """Verify that the projects query is not fulfilled when the query is not authenticated."""
        response = self.client.execute(self.query, variables=self.variables)
        self.assertTrue(
            any("permission" in err.message.lower() for err in response.errors),
            "An unauthenticated query should return a permission error.",
        )
        self.assertIsNone(
            response.data.get("projects"), "An unauthenticated query should not populate the projects object."
        )


class ProjectQueryTest(JSONWebTokenTestCase):

    def setUp(self):
        """Create a user and some data to fetch for authentication testing."""
        self.user = get_user_model().objects.create(username="test")
        self.project = Project.objects.create(name="test project")
        self.query = """
            query Project($id: ID!) {
                project (id: $id) {
                    id
                }
            }
        """
        self.variables = {"id": self.project.id}

    def test_project_fields_match_resolver_args(self):
        """Test that the fields in the `project` definition match the args in the resolver."""
        definition_field_names = list(Query._meta.fields["project"].args.keys())
        resolver_arg_names = list(inspect.signature(Query.resolve_project).parameters.keys())
        resolver_arg_names.remove("self")
        resolver_arg_names.remove("info")
        self.assertEqual(definition_field_names, resolver_arg_names)

    def test_project_authenticated(self):
        """Verify that the project query accessible when the query is authenticated."""
        self.client.authenticate(self.user)
        response = self.client.execute(self.query, variables=self.variables)
        self.assertIsNone(response.errors, "An authenticated query should not return any errors.")
        self.assertIsNotNone(response.data.get("project"), "An authenticated query should populate the project object.")

    def test_project_not_authenticated(self):
        """Verify that the project query is not fulfilled when the query is not authenticated."""
        response = self.client.execute(self.query, variables=self.variables)
        self.assertTrue(
            any("permission" in err.message.lower() for err in response.errors),
            "An unauthenticated query should return a permission error.",
        )
        self.assertIsNone(
            response.data.get("project"), "An unauthenticated query should not populate the project object."
        )


class ItemTypeOptionQueryTest(JSONWebTokenTestCase):

    def setUp(self):
        """Create a user and some data to fetch for authentication testing."""
        self.user = get_user_model().objects.create(username="test")
        self.project = Project.objects.create(name="test project")
        self.query = """
            query ItemTypeOptions($project: ID!) {
                itemTypeOptions(project: $project) {
                    name
                }
            }
        """
        self.variables = {"project": self.project.id}

    def test_item_type_options_authenticated(self):
        """Verify that the item type options query accessible when the query is authenticated."""
        self.client.authenticate(self.user)
        response = self.client.execute(self.query, variables=self.variables)
        self.assertIsNone(response.errors, "An authenticated query should not return any errors.")
        self.assertIsNotNone(
            response.data.get("itemTypeOptions"), "An authenticated query should populate the itemTypeOptions object."
        )

    def test_item_type_options_not_authenticated(self):
        """Verify that the item type options query is not fulfilled when the query is not authenticated."""
        response = self.client.execute(self.query, variables=self.variables)
        self.assertTrue(
            any("permission" in err.message.lower() for err in response.errors),
            "An unauthenticated query should return a permission error.",
        )
        self.assertIsNone(
            response.data.get("itemTypeOptions"),
            "An unauthenticated query should not populate the itemTypeOptions object.",
        )


class ItemStatusOptionsQueryTest(JSONWebTokenTestCase):

    def setUp(self):
        """Create a user and some data to fetch for authentication testing."""
        self.user = get_user_model().objects.create(username="test")
        self.project = Project.objects.create(name="test project")
        self.query = """
            query ItemStatusOptions($project: ID!) {
                itemStatusOptions(project: $project) {
                    name
                }
            }
        """
        self.variables = {"project": self.project.id}

    def test_item_status_options_authenticated(self):
        """Verify that the item status options query accessible when the query is authenticated."""
        self.client.authenticate(self.user)
        response = self.client.execute(self.query, variables=self.variables)
        self.assertIsNone(response.errors, "An authenticated query should not return any errors.")
        self.assertIsNotNone(
            response.data.get("itemStatusOptions"),
            "An authenticated query should populate the itemStatusOptions object.",
        )

    def test_item_status_options_not_authenticated(self):
        """Verify that the item status options query is not fulfilled when the query is not authenticated."""
        response = self.client.execute(self.query, variables=self.variables)
        self.assertTrue(
            any("permission" in err.message.lower() for err in response.errors),
            "An unauthenticated query should return a permission error.",
        )
        self.assertIsNone(
            response.data.get("itemStatusOptions"),
            "An unauthenticated query should not populate the itemStatusOptions object.",
        )


class ItemPriorityOptionsQueryTest(JSONWebTokenTestCase):

    def setUp(self):
        """Create a user and some data to fetch for authentication testing."""
        self.user = get_user_model().objects.create(username="test")
        self.project = Project.objects.create(name="test project")
        self.query = """
            query ItemPriorityOptions($project: ID!) {
                itemPriorityOptions(project: $project) {
                    name
                }
            }
        """
        self.variables = {"project": self.project.id}

    def test_item_priority_options_authenticated(self):
        """Verify that the item priority options query accessible when the query is authenticated."""
        self.client.authenticate(self.user)
        response = self.client.execute(self.query, variables=self.variables)
        self.assertIsNone(response.errors, "An authenticated query should not return any errors.")
        self.assertIsNotNone(
            response.data.get("itemPriorityOptions"),
            "An authenticated query should populate the itemPriorityOptions object.",
        )

    def test_item_priority_options_not_authenticated(self):
        """Verify that the item priority options query is not fulfilled when the query is not authenticated."""
        response = self.client.execute(self.query, variables=self.variables)
        self.assertTrue(
            any("permission" in err.message.lower() for err in response.errors),
            "An unauthenticated query should return a permission error.",
        )
        self.assertIsNone(
            response.data.get("itemPriorityOptions"),
            "An unauthenticated query should not populate the itemPriorityOptions object.",
        )


class ItemsQueryTest(JSONWebTokenTestCase):

    def setUp(self):
        """Create a user and some data to fetch for authentication testing."""
        self.user = get_user_model().objects.create(username="test")
        self.query = """
            query Items {
                items {
                    id
                }
            }
        """
        self.variables = {}

    def test_items_fields_match_resolver_args(self):
        """Test that the fields in the `items` definition match the args in the resolver."""
        definition_field_names = list(Query._meta.fields["items"].args.keys())
        resolver_arg_names = list(inspect.signature(Query.resolve_items).parameters.keys())
        resolver_arg_names.remove("self")
        resolver_arg_names.remove("info")
        self.assertEqual(definition_field_names, resolver_arg_names)

    def test_items_authenticated(self):
        """Verify that the items query accessible when the query is authenticated."""
        self.client.authenticate(self.user)
        response = self.client.execute(self.query, variables=self.variables)
        self.assertIsNone(response.errors, "An authenticated query should not return any errors.")
        self.assertIsNotNone(response.data.get("items"), "An authenticated query should populate the items object.")

    def test_items_not_authenticated(self):
        """Verify that the items query is not fulfilled when the query is not authenticated."""
        response = self.client.execute(self.query, variables=self.variables)
        self.assertTrue(
            any("permission" in err.message.lower() for err in response.errors),
            "An unauthenticated query should return a permission error.",
        )
        self.assertIsNone(response.data.get("items"), "An unauthenticated query should not populate the items object.")


class ItemQueryTest(JSONWebTokenTestCase):

    def setUp(self):
        """Create a user and some data to fetch for authentication testing."""
        self.user = get_user_model().objects.create(username="test")
        self.project = Project.objects.create(name="test project")
        self.item = Item.objects.create(
            name="test item",
            project=self.project,
            item_type=self.project.get_default_item_type(),
            item_status=self.project.get_default_item_status(),
            item_priority=self.project.get_default_item_priority(),
        )
        self.query = """
            query Item($id: ID!) {
                item (id: $id) {
                    id
                }
            }
        """
        self.variables = {"id": self.item.id}

    def test_item_fields_match_resolver_args(self):
        """Test that the fields in the `item` definition match the args in the resolver."""
        definition_field_names = list(Query._meta.fields["item"].args.keys())
        resolver_arg_names = list(inspect.signature(Query.resolve_item).parameters.keys())
        resolver_arg_names.remove("self")
        resolver_arg_names.remove("info")
        self.assertEqual(definition_field_names, resolver_arg_names)

    def test_item_authenticated(self):
        """Verify that the item query accessible when the query is authenticated."""
        self.client.authenticate(self.user)
        response = self.client.execute(self.query, variables=self.variables)
        self.assertIsNone(response.errors, "An authenticated query should not return any errors.")
        self.assertIsNotNone(response.data.get("item"), "An authenticated query should populate the item object.")

    def test_item_not_authenticated(self):
        """Verify that the item query is not fulfilled when the query is not authenticated."""
        response = self.client.execute(self.query, variables=self.variables)
        self.assertTrue(
            any("permission" in err.message.lower() for err in response.errors),
            "An unauthenticated query should return a permission error.",
        )
        self.assertIsNone(response.data.get("item"), "An unauthenticated query should not populate the item object.")
