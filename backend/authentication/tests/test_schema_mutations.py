from django.contrib.auth import get_user_model
from graphql_jwt.testcases import JSONWebTokenTestCase


class TokenAuthMutationTest(JSONWebTokenTestCase):

    def setUp(self):
        """Create a user."""
        self.user = get_user_model().objects.create_user(username="testuser", password="testpassword")
        self.query = """
            mutation TokenAuth($username: String!, $password: String!) {
                tokenAuth(username: $username, password: $password) {
                    token
                }
            }
        """

    def test_token_auth_authenticated(self):
        """Test that a token is returned when using the correct credentials."""
        variables = {"username": "testuser", "password": "testpassword"}
        response = self.client.execute(self.query, variables=variables)
        self.assertIsNone(response.errors, "An authenticated query should not return any errors.")
        self.assertIsNotNone(
            response.data.get("tokenAuth"), "An authenticated query should populate the tokenAuth object."
        )
        self.assertIsNotNone(
            response.data["tokenAuth"].get("token"), "An authenticated query should populate the token field."
        )

    def test_token_auth_not_authenticated(self):
        """Test that an error and no token is returned when invalid credentials are used."""
        variables = {"username": "testuser", "password": "wrongpassword"}
        response = self.client.execute(self.query, variables=variables)
        self.assertIsNotNone(response.errors, "An unauthenticated query should return errors.")
        self.assertIsNone(
            response.data.get("tokenAuth"), "An unauthenticated query should not populate the tokenAuth object."
        )


class VerifyTokenMutationTest(JSONWebTokenTestCase):

    def setUp(self):
        """Create a user and get their token."""
        self.user = get_user_model().objects.create_user(username="testuser", password="testpassword")
        response = self.client.execute(
            """
                mutation TokenAuth($username: String!, $password: String!) {
                    tokenAuth(username: $username, password: $password) {
                        token
                    }
                }
            """,
            variables={"username": "testuser", "password": "testpassword"},
        )
        self.token = response.data["tokenAuth"]["token"]
        self.query = """
            mutation VerifyToken($token: String!) {
                verifyToken(token: $token) {
                    payload
                }
            }
        """

    def test_verify_token_authenticated(self):
        """Test that the verification payload is returned when using a valid token."""
        variables = {"token": self.token}
        response = self.client.execute(self.query, variables=variables)
        self.assertIsNone(response.errors, "An authenticated query should not return any errors.")
        self.assertIsNotNone(
            response.data.get("verifyToken"), "An authenticated query should populate the payload object."
        )

    def test_verify_token_not_authenticated(self):
        """Test that an error and no verification payload is returned when using an invalid token."""
        variables = {"token": "invalid_token"}
        response = self.client.execute(self.query, variables=variables)
        self.assertIsNotNone(response.errors, "An unauthenticated query should return errors.")
        self.assertIsNone(
            response.data.get("verifyToken"), "An unauthenticated query should not populate the verifyToken object."
        )


class RefreshTokenMutationTest(JSONWebTokenTestCase):

    def setUp(self):
        """Create a user and get their token."""
        self.user = get_user_model().objects.create_user(username="testuser", password="testpassword")
        response = self.client.execute(
            """
                mutation TokenAuth($username: String!, $password: String!) {
                    tokenAuth(username: $username, password: $password) {
                        token
                    }
                }
            """,
            variables={"username": "testuser", "password": "testpassword"},
        )
        self.token = response.data["tokenAuth"]["token"]
        self.query = """
            mutation RefreshToken($token: String!) {
                refreshToken(token: $token) {
                    token
                }
            }
        """

    def test_refresh_token_authenticated(self):
        """Test that the refresh token is returned when using a valid token."""
        variables = {"token": self.token}
        response = self.client.execute(self.query, variables=variables)
        self.assertIsNone(response.errors, "An authenticated query should not return any errors.")
        self.assertIsNotNone(
            response.data.get("refreshToken"), "An authenticated query should populate the refreshToken object."
        )
        self.assertEqual(
            response.data["refreshToken"].get("token"),
            self.token,
            "An authenticated query should populate the name field matching the creation data.",
        )

    def test_refresh_token_not_authenticated(self):
        """Test that an error and no refresh token is returned when using an invalid token."""
        variables = {"token": "invalid_token"}
        response = self.client.execute(self.query, variables=variables)
        self.assertIsNotNone(response.errors, "An unauthenticated query should return errors.")
        self.assertIsNone(
            response.data.get("refreshToken"), "An unauthenticated query should not populate the refreshToken object."
        )
