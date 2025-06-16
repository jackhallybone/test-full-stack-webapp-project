import graphene
from graphene_django.types import DjangoObjectType
from organiser.models import Item, Project, ItemType, ItemStatus, ItemLocation
from organiser.schema.filters import filter_items


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


def _resolve_project_descendants(instance, info, name_contains, project, item_type, item_status, item_location):
    """Returns the descendants (which is equivalent to the items) of the project.

    Optionally, filter this queryset by the fields defined in `filters.py:filter_items()`.
    """
    # Getting the children of an item is common, so speculatively prefetch children
    items = instance.get_descendants().prefetch_related("children")
    return filter_items(items, name_contains, project, item_type, item_status, item_location)


class ProjectType(DjangoObjectType):
    """GraphQL Type definition for the Project object, including related field resolvers.

    Computed Fields:
        default_item_type (ItemType): The ItemType object associated with this project that is set as the default.
        default_item_status (ItemStatus): The ItemStatus object associated with this project that is set as the default.
        default_item_location (ItemLocation): The ItemLocation object associated with this project that is set as the default.
        descendants (list): A list of ItemType objects associated with this project.
        items (list): A list of ItemType objects associated with this project. An alias of descendants.
        children (list): A list of ItemType objects associated with this project that do not have a parent Item.
        num_children (int): The number of children Item objects associated with this project.

    Methods:
        resolve_default_item_type():
            Resolves the item_type relationship to get the default type object.
        resolve_default_item_status():
            Resolves the item_status relationship to get the default status object.
        resolve_default_item_location():
            Resolves the item_location relationship to get the default priority object.
        resolve_descendants():
            Resolves the `descendants` relationship on a project to get a list of associated items.
        resolve_items():
            Resolves the `descendants` (via alias `items`) relationship on a project to get a list of associated items.
        resolve_children():
            Resolves the `children` relationship on a project to get a list of associated items.
        resolve_num_children():
            Resolves the total number items with the `children` relationship to a project.
    """

    default_item_type = graphene.Field(ItemTypeType)
    default_item_status = graphene.Field(ItemStatusType)
    default_item_location = graphene.Field(ItemLocationType)
    descendants = graphene.List(
        lambda: ItemType,
        name_contains=graphene.String(),
        project=graphene.ID(),
        item_type=graphene.ID(),
        item_status=graphene.ID(),
        item_location=graphene.ID(),
    )
    items = descendants  # For a project, items is an alias to descendants
    children = graphene.List(
        lambda: ItemType,
        name_contains=graphene.String(),
        project=graphene.ID(),
        item_type=graphene.ID(),
        item_status=graphene.ID(),
        item_location=graphene.ID(),
    )
    num_children = graphene.Int()

    class Meta:
        model = Project
        fields = "__all__"

    def resolve_default_item_type(self, info):
        """Resolves the item_type relationship to get the default type object."""
        return self.get_default_item_type()

    def resolve_default_item_status(self, info):
        """Resolves the item_status relationship to get the default status object."""
        return self.get_default_item_status()

    def resolve_default_item_location(self, info):
        """Resolves the item_location relationship to get the default priority object."""
        return self.get_default_item_location()

    def resolve_descendants(self, info, name_contains=None, project=None, item_type=None, item_status=None, item_location=None):
        """Resolves the `descendants` relationship on a project to get a list of associated items.

        Args:
            info: The GraphQL context and information about the query.
            name_contains (str, optional): Filter to return only items whose name field contains the string.
            project (ID, optional): Filter to return only the items belonging to the given project (id).
            item_type (ID, optional): Filter to return only the items with the given item_type (id).
            item_status (ID, optional): Filter to return only the items with the given item_status (id).
            item_location (ID, optional): Filter to return only the items with the given item_location (id).

        Returns:
            list: A list of `ItemType` objects, filtered based on the parameters.
        """
        return _resolve_project_descendants(self, info, name_contains, project, item_type, item_status, item_location)

    def resolve_items(self, info, name_contains=None, project=None, item_type=None, item_status=None, item_location=None):
        """Resolves the `descendants` (via alias `items`) relationship on a project to get a list of associated items.

        Args:
            info: The GraphQL context and information about the query.
            name_contains (str, optional): Filter to return only items whose name field contains the string.
            project (ID, optional): Filter to return only the items belonging to the given project (id).
            item_type (ID, optional): Filter to return only the items with the given item_type (id).
            item_status (ID, optional): Filter to return only the items with the given item_status (id).
            item_location (ID, optional): Filter to return only the items with the given item_location (id).

        Returns:
            list: A list of `ItemType` objects, filtered based on the parameters.
        """
        return _resolve_project_descendants(self, info, name_contains, project, item_type, item_status, item_location)

    def resolve_children(self, info, name_contains=None, project=None, item_type=None, item_status=None, item_location=None):
        """Resolves the `children` relationship on a project to get a list of associated items.

        Args:
            info: The GraphQL context and information about the query.
            name_contains (str, optional): Filter to return only items whose name field contains the string.
            project (ID, optional): Filter to return only the items belonging to the given project (id).
            item_type (ID, optional): Filter to return only the items with the given item_type (id).
            item_status (ID, optional): Filter to return only the items with the given item_status (id).
            item_location (ID, optional): Filter to return only the items with the given item_location (id).

        Returns:
            list: A list of `ItemType` objects, filtered based on the parameters.
        """
        # Getting the children of an item is common, so speculatively prefetch children
        items = self.get_children().prefetch_related("children")
        return filter_items(items, name_contains, project, item_type, item_status, item_location)

    def resolve_num_children(self, info):
        """Resolves the total number items with the `children` relationship to a project."""
        return self.get_num_children()


class ItemType(DjangoObjectType):
    """GraphQL Type definition for the Item object, including related field resolvers.

    Fields:
        ancestors (list): A list of ItemType objects that are ancestors of this item.
        descendants (list): A list of ItemType objects associated with this item.
        children (list): A list of ItemType objects that are direct children of this item.
        num_children (int): The number of children Item objects associated with this item.

    Methods:
        resolve_ancestors():
            Resolves the `ancestors` relationship on an item to get a list of the items ancestors.
        resolve_descendants():
            Resolves the `descendants` relationship on an item to get a list of associated items.
        resolve_children():
            Resolves the `children` relationship on an item to get a list of associated items.
        resolve_num_children():
            Resolves the total number items with the `children` relationship to an item.
    """

    ancestors = graphene.List(
        lambda: ItemType,
        name_contains=graphene.String(),
        project=graphene.ID(),
        item_type=graphene.ID(),
        item_status=graphene.ID(),
        item_location=graphene.ID(),
    )
    descendants = graphene.List(
        lambda: ItemType,
        name_contains=graphene.String(),
        project=graphene.ID(),
        item_type=graphene.ID(),
        item_status=graphene.ID(),
        item_location=graphene.ID(),
    )
    children = graphene.List(
        lambda: ItemType,
        name_contains=graphene.String(),
        project=graphene.ID(),
        item_type=graphene.ID(),
        item_status=graphene.ID(),
        item_location=graphene.ID(),
    )
    num_children = graphene.Int()

    class Meta:
        model = Item
        fields = "__all__"

    def resolve_ancestors(self, info, name_contains=None, project=None, item_type=None, item_status=None, item_location=None):
        """Resolves the `ancestors` relationship on an item to get a list of the items ancestors.

        Args:
            info: The GraphQL context and information about the query.
            name_contains (str, optional): Filter to return only items whose name field contains the string.
            project (ID, optional): Filter to return only the items belonging to the given project (id).
            item_type (ID, optional): Filter to return only the items with the given item_type (id).
            item_status (ID, optional): Filter to return only the items with the given item_status (id).
            item_location (ID, optional): Filter to return only the items with the given item_location (id).

        Returns:
            list: A list of `ItemType` objects, filtered based on the parameters.
        """
        items = self.get_ancestors()
        return filter_items(items, name_contains, project, item_type, item_status, item_location)

    def resolve_descendants(self, info, name_contains=None, project=None, item_type=None, item_status=None, item_location=None):
        """Resolves the `descendants` relationship on an item to get a list of associated items.

        Args:
            info: The GraphQL context and information about the query.
            name_contains (str, optional): Filter to return only items whose name field contains the string.
            project (ID, optional): Filter to return only the items belonging to the given project (id).
            item_type (ID, optional): Filter to return only the items with the given item_type (id).
            item_status (ID, optional): Filter to return only the items with the given item_status (id).
            item_location (ID, optional): Filter to return only the items with the given item_location (id).

        Returns:
            list: A list of `ItemType` objects, filtered based on the parameters.
        """
        items = self.get_descendants()
        return filter_items(items, name_contains, project, item_type, item_status, item_location)

    def resolve_children(self, info, name_contains=None, project=None, item_type=None, item_status=None, item_location=None):
        """Resolves the `children` relationship on an item to get a list of associated items.

        Args:
            info: The GraphQL context and information about the query.
            name_contains (str, optional): Filter to return only items whose name field contains the string.
            project (ID, optional): Filter to return only the items belonging to the given project (id).
            item_type (ID, optional): Filter to return only the items with the given item_type (id).
            item_status (ID, optional): Filter to return only the items with the given item_status (id).
            item_location (ID, optional): Filter to return only the items with the given item_location (id).

        Returns:
            list: A list of `ItemType` objects, filtered based on the parameters.
        """
        items = self.get_children()
        return filter_items(items, name_contains, project, item_type, item_status, item_location)

    def resolve_num_children(self, info):
        """Resolves the total number items with the `children` relationship to an item."""
        return self.get_num_children()
