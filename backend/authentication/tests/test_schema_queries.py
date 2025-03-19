from django.contrib.auth import get_user_model
from graphql_jwt.testcases import JSONWebTokenTestCase


class ProfileQuery(JSONWebTokenTestCase):

    def setUp(self):
        """Create a user and some data to fetch for authentication testing."""
        self.user = get_user_model().objects.create_user(username="testuser", password="testpassword")
        self.query = """
            query {
                profile {
                    username
                }
            }
        """
        self.variables = {}

    def test_query_profile_authenticated(self):
        """Verify that the profile is returned when the query is authenticated."""
        self.client.authenticate(self.user)
        response = self.client.execute(self.query, variables=self.variables)
        self.assertIsNone(response.errors, "An authenticated query should not return any errors.")
        self.assertIsNotNone(response.data.get("profile"), "An authenticated query should populate the profile object.")
        self.assertEqual(
            response.data["profile"].get("username"),
            self.user.username,
            "An authenticated query should populate the username field matching the current user.",
        )

    def test_query_profile_not_authenticated(self):
        """Verify that the profile is not returned when the query is not authenticated."""
        response = self.client.execute(self.query, variables=self.variables)
        self.assertTrue(
            any("permission" in err.message.lower() for err in response.errors),
            "An unauthenticated query should return a permission error.",
        )
        self.assertIsNone(
            response.data.get("profile"), "An unauthenticated query should not populate the profile object."
        )
