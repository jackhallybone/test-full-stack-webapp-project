import graphene
from django.contrib.auth import get_user_model
from graphql_jwt.testcases import JSONWebTokenTestCase
from django.db.models.signals import post_save

from organiser.models import Item, Project, ItemTypeOption, ItemStatusOption, ItemPriorityOption
from organiser.schema.mutations import Mutation
from organiser.signals import create_default_project_settings


class MutationTest(JSONWebTokenTestCase):

    def test_schema(self):
        """Check that the schema builds."""
        schema = graphene.Schema(mutation=Mutation)
        self.assertIsNotNone(schema)


class CreateProjectMutationTest(JSONWebTokenTestCase):

    def setUp(self):
        """Create a user."""
        self.user = get_user_model().objects.create_user(username="testuser", password="testpassword")
        self.query = """
            mutation CreateProject($input: CreateProjectInput!) {
                createProject(input: $input) {
                    project {
                        name
                    }
                }
            }
        """
        self.variables = {"input": {"name": "test name"}}

    def test_create_project_authenticated(self):
        """Test that a project is created when using the correct credentials."""
        self.client.authenticate(self.user)
        response = self.client.execute(self.query, variables=self.variables)
        self.assertIsNone(response.errors, "An authenticated query should not return any errors.")
        self.assertIsNotNone(
            response.data.get("createProject"), "An authenticated query should populate the createProject object."
        )
        self.assertEqual(
            response.data["createProject"]["project"].get("name"),
            self.variables["input"]["name"],
            "An authenticated query should populate the name field matching the creation data.",
        )
        self.assertEqual(
            Project.objects.all().count(), 1, "An authenticated query should have created the project in the database."
        )

    def test_create_project_not_authenticated(self):
        """Test that an error is returned when invalid credentials are used."""
        # Do not authenticate
        response = self.client.execute(self.query, variables=self.variables)
        self.assertTrue(
            any("permission" in err.message.lower() for err in response.errors),
            "An unauthenticated query should return a permission error.",
        )
        self.assertIsNone(
            response.data.get("createProject"), "An unauthenticated query should not populate the createProject object."
        )
        self.assertEqual(
            Project.objects.all().count(),
            0,
            "An unauthenticated query should not have created the project in the database.",
        )


class UpdateProjectTest(JSONWebTokenTestCase):

    def setUp(self):
        """Create a user."""
        self.user = get_user_model().objects.create_user(username="testuser", password="testpassword")
        self.original_project = Project.objects.create(name="original name")
        self.query = """
            mutation ($id: ID!, $input: PartialUpdateProjectInput!) {
                updateProject(id: $id, input: $input) {
                    project {
                        name
                    }
                }
            }
        """
        self.variables = {"id": self.original_project.id, "input": {"name": "new name"}}

    def test_update_project_authenticated(self):
        """Test that a project is updated when using the correct credentials."""
        self.client.authenticate(self.user)
        response = self.client.execute(self.query, variables=self.variables)
        self.assertIsNone(response.errors, "An authenticated query should not return any errors.")
        self.assertIsNotNone(
            response.data.get("updateProject"), "An authenticated query should populate the updateProject object."
        )
        self.assertEqual(
            response.data["updateProject"]["project"]["name"],
            self.variables["input"]["name"],
            "An authenticated query should populate the name field matching the updated data.",
        )
        self.assertEqual(
            Project.objects.get(id=self.original_project.id).name,
            self.variables["input"]["name"],
            "An authenticated query should have updated the project in the database.",
        )

    def test_update_project_not_authenticated(self):
        """Test that an error is returned when invalid credentials are used."""
        # Do not authenticate
        response = self.client.execute(self.query, variables=self.variables)
        self.assertTrue(
            any("permission" in err.message.lower() for err in response.errors),
            "An unauthenticated query should return a permission error.",
        )
        self.assertIsNone(
            response.data.get("updateProject"), "An unauthenticated query should not populate the updateProject object."
        )
        self.assertEqual(
            Project.objects.get(id=self.original_project.id).name,
            "original name",
            "An unauthenticated query should not have updated the project in the database.",
        )


class DeleteProjectTest(JSONWebTokenTestCase):

    def setUp(self):
        """Create a user."""
        self.user = get_user_model().objects.create_user(username="testuser", password="testpassword")
        original_project = Project.objects.create(name="original name")
        self.query = """
            mutation ($id: ID!) {
                deleteProject(id: $id) {
                    success
                }
            }
        """
        self.variables = {"id": original_project.id}

    def test_delete_project_authenticated(self):
        """Test that a project is deleted when using the correct credentials."""
        self.client.authenticate(self.user)
        response = self.client.execute(self.query, variables=self.variables)
        self.assertIsNone(response.errors, "An authenticated query should not return any errors.")
        self.assertIsNotNone(
            response.data.get("deleteProject"), "An authenticated query should populate the deleteProject object."
        )
        self.assertTrue(
            response.data["deleteProject"]["success"],
            "An authenticated query should populate the name field matching the updated data.",
        )
        self.assertEqual(
            Project.objects.all().count(), 0, "An authenticated query should have deleted the project in the database."
        )

    def test_delete_project_not_authenticated(self):
        """Test that an error is returned when invalid credentials are used."""
        # Do not authenticate
        response = self.client.execute(self.query, variables=self.variables)
        self.assertTrue(
            any("permission" in err.message.lower() for err in response.errors),
            "An unauthenticated query should return a permission error.",
        )
        self.assertIsNone(
            response.data.get("deleteProject"), "An unauthenticated query should not populate the deleteProject object."
        )
        self.assertEqual(
            Project.objects.all().count(),
            1,
            "An unauthenticated query should not have deleted the project in the database.",
        )


class CreateItemMutationTest(JSONWebTokenTestCase):

    def setUp(self):
        """Create a user and some data."""
        self.user = get_user_model().objects.create_user(username="testuser", password="testpassword")
        post_save.disconnect(create_default_project_settings, sender=Project)
        project = Project.objects.create(name="project")
        project_item_type_task = ItemTypeOption.objects.create(project=project, name="Task", order=4, nestable=True, default=True)
        project_item_status_to_do = ItemStatusOption.objects.create(project=project, name="To Do", order=1, default=True)
        project_item_priority_medium = ItemPriorityOption.objects.create(project=project, name="Medium", order=2, default=True)
        parent = Item.objects.create(
            name="Parent Item",
            project=project,
            item_type=project_item_type_task,
            item_status=project_item_status_to_do,
            item_priority=project_item_priority_medium,
        )
        self.query = """
            mutation CreateItem($input: CreateItemInput!) {
                createItem(input: $input) {
                    item {
                        name
                    }
                }
            }
        """
        self.variables = {
            "input": {
                "name": "item name",
                "project": project.id,
                "parent": parent.id,
                "itemType": project_item_type_task.id,
                "itemStatus": project_item_status_to_do.id,
                "itemPriority": project_item_priority_medium.id
            }
        }

    def tearDown(self):
        post_save.connect(create_default_project_settings, sender=Project)

    def test_create_item_authenticated(self):
        """Test that a item is created when using the correct credentials."""
        self.client.authenticate(self.user)
        response = self.client.execute(self.query, variables=self.variables)
        self.assertIsNone(response.errors, "An authenticated query should not return any errors.")
        self.assertIsNotNone(
            response.data.get("createItem"), "An authenticated query should populate the createItem object."
        )
        self.assertEqual(
            response.data["createItem"]["item"].get("name"),
            self.variables["input"]["name"],
            "An authenticated query should populate the name field matching the creation data.",
        )
        self.assertEqual(
            Item.objects.all().count(), 2, "An authenticated query should have created the (second) item in the database."
        )

    def test_create_item_not_authenticated(self):
        """Test that an error is returned when invalid credentials are used."""
        # Do not authenticate
        response = self.client.execute(self.query, variables=self.variables)
        self.assertTrue(
            any("permission" in err.message.lower() for err in response.errors),
            "An unauthenticated query should return a permission error.",
        )
        self.assertIsNone(
            response.data.get("createItem"), "An unauthenticated query should not populate the createItem object."
        )
        self.assertEqual(
            Item.objects.all().count(), 1, "An unauthenticated query should not have created the (second) item in the database."
        )


class UpdateItemTest(JSONWebTokenTestCase):

    def setUp(self):
        """Create a user and data."""
        self.user = get_user_model().objects.create_user(username="testuser", password="testpassword")
        post_save.disconnect(create_default_project_settings, sender=Project)
        project = Project.objects.create(name="project")
        project_item_type_task = ItemTypeOption.objects.create(project=project, name="Task", order=4, nestable=True, default=True)
        project_item_status_to_do = ItemStatusOption.objects.create(project=project, name="To Do", order=1, default=True)
        project_item_priority_medium = ItemPriorityOption.objects.create(project=project, name="Medium", order=2, default=True)
        parent = Item.objects.create(
            name="parent item",
            project=project,
            item_type=project_item_type_task,
            item_status=project_item_status_to_do,
            item_priority=project_item_priority_medium
        )
        self.item = Item.objects.create(
            name="original name",
            project=project,
            parent=parent,
            item_type=project_item_type_task,
            item_status=project_item_status_to_do,
            item_priority=project_item_priority_medium
        )

        self.query = """
            mutation ($id: ID!, $input: PartialUpdateItemInput!) {
                updateItem(id: $id, input: $input) {
                    item {
                        name
                    }
                }
            }
        """
        self.variables = {
            "id": self.item.id,
            "input": {
                "name": "new name",
                "project": project.id,
                "parent": parent.id,
                "itemType": project_item_type_task.id,
                "itemStatus": project_item_status_to_do.id,
                "itemPriority": project_item_priority_medium.id,
            },
        }

    def tearDown(self):
        post_save.connect(create_default_project_settings, sender=Project)

    def test_update_item_authenticated(self):
        """Test that a item is updated when using the correct credentials."""
        self.client.authenticate(self.user)
        response = self.client.execute(self.query, variables=self.variables)
        self.assertIsNone(response.errors, "An authenticated query should not return any errors.")
        self.assertIsNotNone(
            response.data.get("updateItem"), "An authenticated query should populate the updateItem object."
        )
        self.assertEqual(
            response.data["updateItem"]["item"]["name"],
            self.variables["input"]["name"],
            "An authenticated query should populate the name field matching the updated data.",
        )
        self.assertEqual(
            Item.objects.get(id=self.item.id).name,
            self.variables["input"]["name"],
            "An authenticated query should have updated the item in the database.",
        )

    def test_update_item_not_authenticated(self):
        """Test that an error is returned when invalid credentials are used."""
        # Do not authenticate
        response = self.client.execute(self.query, variables=self.variables)
        self.assertTrue(
            any("permission" in err.message.lower() for err in response.errors),
            "An unauthenticated query should return a permission error.",
        )
        self.assertIsNone(
            response.data.get("updateItem"), "An unauthenticated query should not populate the updateItem object."
        )
        self.assertEqual(
            Item.objects.get(id=self.item.id).name,
            "original name",
            "An unauthenticated query should not have updated the item in the database.",
        )


class DeleteItemTest(JSONWebTokenTestCase):

    def setUp(self):
        """Create a user and data."""
        self.user = get_user_model().objects.create_user(username="testuser", password="testpassword")
        post_save.disconnect(create_default_project_settings, sender=Project)
        project = Project.objects.create(name="project")
        project_item_type_task = ItemTypeOption.objects.create(project=project, name="Task", order=4, nestable=True, default=True)
        project_item_status_to_do = ItemStatusOption.objects.create(project=project, name="To Do", order=1, default=True)
        project_item_priority_medium = ItemPriorityOption.objects.create(project=project, name="Medium", order=2, default=True)
        item = Item.objects.create(
            name="original name",
            project=project,
            item_type=project_item_type_task,
            item_status=project_item_status_to_do,
            item_priority=project_item_priority_medium
        )
        self.query = """
            mutation ($id: ID!) {
                deleteItem(id: $id) {
                    success
                }
            }
        """
        self.variables = {"id": item.id}

    def tearDown(self):
        post_save.connect(create_default_project_settings, sender=Project)

    def test_delete_item_authenticated(self):
        """Test that a item is deleted when using the correct credentials."""
        self.client.authenticate(self.user)
        response = self.client.execute(self.query, variables=self.variables)
        self.assertIsNone(response.errors, "An authenticated query should not return any errors.")
        self.assertIsNotNone(
            response.data.get("deleteItem"), "An authenticated query should populate the deleteItem object."
        )
        self.assertTrue(
            response.data["deleteItem"]["success"],
            "An authenticated query should populate the name field matching the updated data.",
        )
        self.assertEqual(
            Item.objects.all().count(), 0, "An authenticated query should have deleted the item in the database."
        )

    def test_delete_item_not_authenticated(self):
        """Test that an error is returned when invalid credentials are used."""
        # Do not authenticate
        response = self.client.execute(self.query, variables=self.variables)
        self.assertTrue(
            any("permission" in err.message.lower() for err in response.errors),
            "An unauthenticated query should return a permission error.",
        )
        self.assertIsNone(
            response.data.get("deleteItem"), "An unauthenticated query should not populate the deleteItem object."
        )
        self.assertEqual(
            Item.objects.all().count(), 1, "An unauthenticated query should not have deleted the item in the database."
        )
