import graphene
from authentication.schema.mutations import Mutation as AuthMutation
from authentication.schema.queries import Query as AuthQuery
from organiser.schema.mutations import Mutation as OrganiserMutation
from organiser.schema.queries import Query as OrganiserQuery


class Query(AuthQuery, OrganiserQuery):
    """Combines the Query classes for each app into a single Query object."""

    pass


class Mutation(AuthMutation, OrganiserMutation):
    """Combines the Mutation classes for each app into a single Mutation object."""

    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
