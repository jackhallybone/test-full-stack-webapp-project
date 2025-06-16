import graphene
from organiser.schema.mutations import Mutation as OrganiserMutation
from organiser.schema.queries import Query as OrganiserQuery


class Query(OrganiserQuery):
    """Combines the Query classes for each app into a single Query object."""

    pass


class Mutation(OrganiserMutation):
    """Combines the Mutation classes for each app into a single Mutation object."""

    pass


schema = graphene.Schema(query=Query, mutation=Mutation)