import graphene
from graphql_jwt.decorators import login_required
from organiser.models import Item, Project
from organiser.schema.filters import filter_items, filter_projects
from organiser.schema.types import ItemTypeOptionType, ItemStatusOptionType, ItemPriorityOptionType, ItemType, ProjectType


class Query(graphene.ObjectType):
    """GraphQL Query definition for the Organiser app.

    Fields:
        projects (list): A list of ProjectType objects.
        project (ProjectType): A specific ProjectType object.
        item_type_options (list): A list of the possible item type options for a particular project and it's children.
        item_status_options (list): A list of the possible item status options for a particular project and it's children.
        item_priority_options (list): A list of the possible item priority options for a particular project and it's children.
        items (list): A list of ItemType objects.
        item (ItemType): A specific ItemType object.

    Methods:
        resolve_projects():
            Resolves all projects.
        resolve_project():
            Resolves a specific project.
        resolve_item_type_options():
            Resolves all the item_type options.
        resolve_item_status_options():
            Resolves all the item_status options.
        resolve_item_priority_options():
            Resolves all the item_priority options.
        resolve_items():
            Resolves all items.
        resolve_item():
            Resolves a specific item.
    """

    projects = graphene.List(
        ProjectType,
        name_contains=graphene.String(),
    )
    project = graphene.Field(ProjectType, id=graphene.ID())
    item_type_options = graphene.List(
        ItemTypeOptionType,
        project=graphene.ID(),
    )
    item_status_options = graphene.List(
        ItemStatusOptionType,
        project=graphene.ID(),
    )
    item_priority_options = graphene.List(
        ItemPriorityOptionType,
        project=graphene.ID(),
    )
    items = graphene.List(
        ItemType,
        name_contains=graphene.String(),
        project=graphene.ID(),
        item_type=graphene.ID(),
        item_status=graphene.ID(),
        item_priority=graphene.ID(),
    )
    item = graphene.Field(ItemType, id=graphene.ID())

    @login_required
    def resolve_projects(self, info, name_contains=None):
        """Resolves all projects.

        Args:
            info: The GraphQL context and information about the query.
            name_contains (str, optional): Filter to return only items whose name field contains the string.

        Returns:
            list: A list of `ProjectType` objects, filtered based on the parameters.

        Raises:
            PermissionDenied: If the query/user is not authenticated.
        """
        projects = Project.objects.all()
        return filter_projects(projects, name_contains)

    @login_required
    def resolve_project(self, info, id):
        """Resolves a specific project.

        Args:
            info: The GraphQL context and information about the query.
            id (ID): The ID of the specific project to resolve.

        Returns:
            ProjectType: A specific `ProjectType` object.

        Raises:
            PermissionDenied: If the query/user is not authenticated.
        """
        return Project.objects.get(id=id)

    @login_required
    def resolve_item_type_options(self, info, project):
        """Resolves a list of the possible item type options for a particular project and it's children.

        Returns:
            list: A list of `ItemType` objects.

        Raises:
            PermissionDenied: If the query/user is not authenticated.
        """
        return Project.objects.get(id=project).item_types.all()

    @login_required
    def resolve_item_status_options(self, info, project):
        """Resolves a list of the possible item status options for a particular project and it's children.

        Returns:
            list: A list of `ItemStatusOption` objects.

        Raises:
            PermissionDenied: If the query/user is not authenticated.
        """
        return Project.objects.get(id=project).item_statuses.all()

    @login_required
    def resolve_item_priority_options(self, info, project):
        """Resolves a list of the possible item priority options for a particular project and it's children.

        Returns:
            list: A list of `ItemPriorityOption` objects.

        Raises:
            PermissionDenied: If the query/user is not authenticated.
        """
        return Project.objects.get(id=project).item_priorities.all()

    @login_required
    def resolve_items(self, info, name_contains=None, project=None, item_type=None, item_status=None, item_priority=None):
        """Resolves all items.

        Args:
            info: The GraphQL context and information about the query.
            name_contains (str, optional): Filter to return only items whose name field contains the string.
            project (ID, optional): Filter to return only the items belonging to the given project (id).
            item_type (ID, optional): Filter to return only the items with the given item_type (id).
            item_status (ID, optional): Filter to return only the items with the given item_status (id).
            item_priority (ID, optional): Filter to return only the items with the given item_priority (id).

        Returns:
            list: A list of `ItemType` objects, filtered based on the parameters.

        Raises:
            PermissionDenied: If the query/user is not authenticated.
        """
        # Getting the children of an item is common, so speculatively prefetch children
        items = Item.objects.prefetch_related("children").all()
        return filter_items(items, name_contains, project, item_type, item_status, item_priority)

    @login_required
    def resolve_item(self, info, id):
        """Resolves a specific item.

        Args:
            info: The GraphQL context and information about the query.
            id (ID): The ID of the specific item to resolve.

        Returns:
            ItemType: A specific `ItemType` object.

        Raises:
            PermissionDenied: If the query/user is not authenticated.
        """
        # Getting the children of an item is common, so speculatively prefetch children
        return Item.objects.prefetch_related("children").get(id=id)
