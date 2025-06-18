import graphene
from graphene_django.types import DjangoObjectType

from items.graphql.inputs import ItemFilterInput
from items.models import Item, ItemLocation, ItemStatus, ItemType, Project


class ProjectType(DjangoObjectType):
    item_types = graphene.List(lambda: ItemTypeType)
    item_statuses = graphene.List(lambda: ItemStatusType)
    item_locations = graphene.List(lambda: ItemLocationType)
    default_item_type = graphene.Field(lambda: ItemTypeType)
    default_item_status = graphene.Field(lambda: ItemStatusType)
    default_item_location = graphene.Field(lambda: ItemLocationType)
    descendants = graphene.List(
        lambda: ItemType, filters=graphene.Argument(ItemFilterInput)
    )
    num_descendants = graphene.Int(filters=graphene.Argument(ItemFilterInput))
    items = descendants  # alias
    num_items = num_descendants  # alias
    children = graphene.List(
        lambda: ItemType, filters=graphene.Argument(ItemFilterInput)
    )
    num_children = graphene.Int(filters=graphene.Argument(ItemFilterInput))

    class Meta:
        model = Project
        fields = "__all__"

    def resolve_item_types(self, info):
        """Resolve all `ItemType`s for the current `Project`."""
        return self.get_item_types()

    def resolve_default_item_type(self, info):
        """Resolve the `ItemType` marked as default for the current `Project`."""
        return self.get_default_item_type()

    def resolve_item_statuses(self, info):
        """Resolve all `ItemStatus`es for the current `Project`."""
        return self.get_item_statuses()

    def resolve_default_item_status(self, info):
        """Resolve the `ItemStatus` marked as default for the current `Project`."""
        return self.get_default_item_status()

    def resolve_item_locations(self, info):
        """Resolve all `ItemLocation`s for the current `Project`."""
        return self.get_item_locations()

    def resolve_default_item_location(self, info):
        """Resolve the `ItemLocation` marked as default for the current `Project`."""
        return self.get_default_item_location()

    def resolve_descendants(self, info, filters=None):
        """Resolve all `Item`s matching the filter that are descendants of (assigned to) the current `Project`."""
        filters = filters or {}
        return self.get_descendants(**filters)

    def resolve_num_descendants(self, info, filters=None):
        """Resolve the number of `Item`s matching the filter that are descendants of (assigned to) this `Project`."""
        filters = filters or {}
        return self.get_num_descendants(**filters)

    resolve_get_items = resolve_descendants  # alias
    resolve_get_num_items = resolve_num_descendants  # alias

    def resolve_children(self, info, filters=None):
        """Resolve the `Item`s matching the filter that are direct children (do not have a parent `Item`) of this `Project`."""
        filters = filters or {}
        return self.get_children(**filters)

    def resolve_num_children(self, info, filters=None):
        """Resolve the number of `Item`s matching the filter that are direct children (do not have a parent `Item`) of this `Project`."""
        filters = filters or {}
        return self.get_num_children(**filters)


class ItemTypeType(DjangoObjectType):
    class Meta:
        model = ItemType
        fields = "__all__"


class ItemStatusType(DjangoObjectType):
    class Meta:
        model = ItemStatus
        fields = "__all__"


class ItemLocationType(DjangoObjectType):
    class Meta:
        model = ItemLocation
        fields = "__all__"


class ItemType(DjangoObjectType):
    """GraphQL Type definition for the Item object, including related field resolvers."""

    ancestors = graphene.List(
        lambda: ItemType,
    )
    num_ancestors = graphene.Int()
    descendants = graphene.List(
        lambda: ItemType, filters=graphene.Argument(ItemFilterInput)
    )
    num_descendants = graphene.Int(filters=graphene.Argument(ItemFilterInput))
    children = graphene.List(
        lambda: ItemType, filters=graphene.Argument(ItemFilterInput)
    )
    num_children = graphene.Int(filters=graphene.Argument(ItemFilterInput))

    class Meta:
        model = Item
        fields = "__all__"

    def resolve_ancestors(self, info):
        """Resolve all `Item`s that are ancestors of this `Item, ordered from root to this item's parent."""
        return self.get_ancestors()

    def resolve_num_ancestors(self, info):
        """Resolve the number of `Item`s that are ancestors of this `Item`."""
        return self.get_ancestors()

    def resolve_descendants(self, info, filters=None):
        """Resolve all `Item`s matching the filter that are descendants of this `Item."""
        filters = filters or {}
        return self.get_descendants(**filters)

    def resolve_num_descendants(self, info, filters=None):
        """Resolve the number of `Item`s matching the filter that are descendants of this `Item`."""
        filters = filters or {}
        return self.get_num_descendants(**filters)

    def resolve_children(self, info, filters=None):
        """Resolve the `Item`s matching the filter that are direct children of this `Item`."""
        filters = filters or {}
        return self.get_children(**filters)

    def resolve_num_children(self, info, filters=None):
        """Resolve the number of `Item`s matching the filter that are direct children of this `Item`."""
        filters = filters or {}
        return self.get_num_children(**filters)
