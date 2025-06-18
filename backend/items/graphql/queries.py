import graphene

from items.graphql.crud import BaseCRUD
from items.graphql.inputs import ItemFilterInput, ProjectFilterInput
from items.graphql.types import ItemType, ProjectType
from items.models import Item, Project


class Query(graphene.ObjectType):

    projects = graphene.List(
        lambda: ProjectType, filters=graphene.Argument(ProjectFilterInput)
    )
    project = graphene.Field(lambda: ProjectType, id=graphene.ID())
    items = graphene.List(lambda: ItemType, filters=graphene.Argument(ItemFilterInput))
    item = graphene.Field(lambda: ItemType, id=graphene.ID())

    def resolve_projects(self, info, filters=None):
        """Resolve all `Project`s that match the filter."""
        filters = filters or {}
        return BaseCRUD(Project).read_all().filter_projects(**filters)

    def resolve_project(self, info, id):
        """Resolve a `Project` by its id."""
        return BaseCRUD(Project).read_one(id)

    def resolve_items(self, info, filters=None):
        """Resolve all `Item`s that match the filter."""
        filters = filters or {}
        return BaseCRUD(Item).read_all().filter_items(**filters)

    def resolve_item(self, info, id):
        """Resolve an `Item` by its id."""
        return BaseCRUD(Item).read_one(id)
