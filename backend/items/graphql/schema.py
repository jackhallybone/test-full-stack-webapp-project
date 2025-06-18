import graphene

from items.graphql.mutations import Mutation
from items.graphql.queries import Query

schema = graphene.Schema(query=Query, mutation=Mutation)
