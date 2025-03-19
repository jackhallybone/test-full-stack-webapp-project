import graphene
from django.contrib.auth.models import User
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required


class ProfileType(DjangoObjectType):
    """GraphQL Type definition for the user profile object.

    Fields:
        username (str): The username of the user.
    """

    class Meta:
        model = User
        fields = ("username",)


class Query(graphene.ObjectType):
    """GraphQL Query definition for the Authentication app.

    Fields:
        profile(ProfileType): The profile of the authenticated user.

    Methods:
        resolve_profile():
            Resolves the profile of the authenticated user.
    """

    profile = graphene.Field(ProfileType)

    @login_required
    def resolve_profile(self, info):
        """Resolves the currently authenticated user.

        Returns:
            ProfileType: An instance of the logged in user object.

        Raises:
            PermissionDenied: If the query/user is not authenticated.
        """
        return info.context.user
