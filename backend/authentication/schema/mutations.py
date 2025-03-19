import graphene
import graphql_jwt


class Mutation(graphene.ObjectType):
    """GraphQL Mutation definition for the Authentication app.

    Fields:
        token_auth (ObtainJSONWebToken.Field): Authenticates a user and returns a JWT token.
        verify_token (Verify.Field): Verifies the validity of a JWT token.
        refresh_token (Refresh.Field): Refreshes an expired or near-expired JWT token.
    """

    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
