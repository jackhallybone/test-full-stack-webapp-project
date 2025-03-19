import graphene
from graphql_jwt.decorators import login_required
from organiser.models import Item, Project, ItemTypeOption, ItemStatusOption, ItemPriorityOption
from organiser.schema.types import ItemType, ProjectType


class CreateProjectInput(graphene.InputObjectType):
    """Input object type for creating a new project.

    Fields:
        name (str): The name of the project. Required.
        description (str): A description of the project.
    """

    name = graphene.String(required=True)
    description = graphene.String()


class PartialUpdateProjectInput(graphene.InputObjectType):
    """Input object type for partially updating an existing project.

    Fields:
        name (str, optional): The new name for the project.
        description (str, optional): A new description for the project.
    """

    name = graphene.String()
    description = graphene.String()


class CreateItemInput(graphene.InputObjectType):
    """Input object type for creating a new item.

    Fields:
        name (str): The name of the item.
        changelog (str, optional): A short description of the work done.
        description (str, optional): A general description of the item.
        requirements (str, optional): A description of the work that needs to be done.
        outcome (str, optional): A description of the work that has been done.
        project (ID): The ID of the project the item belongs to.
        parent (ID, optional): The ID of the parent item.
        item_type (ID): The ID of the item's item_type.
        item_status (ID): The ID of the item's item_status.
        item_priority (ID): The ID of the item's item_priority.
        kanban_row_order (Int, optional): The index/order of the item in the kanban column.
    """

    name = graphene.String(required=True)
    changelog = graphene.String()
    description = graphene.String()
    requirements = graphene.String()
    outcome = graphene.String()
    project = graphene.ID(required=True)
    parent = graphene.ID()
    item_type = graphene.ID(required=True)
    item_status = graphene.ID(required=True)
    item_priority = graphene.ID(required=True)
    kanban_row_order = graphene.Int()

class PartialUpdateItemInput(graphene.InputObjectType):
    """Input object type for partially updating an existing item.

    Fields:
        name (str): The name of the item.
        changelog (str): A short description of the work done.
        description (str): A general description of the item.
        requirements (str): A description of the work that needs to be done.
        outcome (str): A description of the work that has been done.
        project (ID): The ID of the project the item belongs to.
        parent (ID): The ID of the parent item.
        item_type (ID): The ID of the item's item_type.
        item_status (ID): The ID of the item's item_status.
        item_priority (ID): The ID of the item's item_priority.
        kanban_row_order (Int): The index/order of the item in the kanban column.
    """

    name = graphene.String()
    changelog = graphene.String()
    description = graphene.String()
    requirements = graphene.String()
    outcome = graphene.String()
    project = graphene.ID()
    parent = graphene.ID()
    item_type = graphene.ID()
    item_status = graphene.ID()
    item_priority = graphene.ID()
    kanban_row_order = graphene.Int()


class CreateProject(graphene.Mutation):
    """Mutation for creating a new project.

    Arguments:
        input (CreateProjectInput): Input object containing the details of the project to create.

    Fields:
        project (ProjectType): The newly created project object.

    Methods:
        mutate():
            Create a new project in the database with the given input field data.

    Returns:
        CreateProject: An instance of the mutation class containing the created project as a field.

    Raises:
        PermissionDenied : If the query/user is not authenticated.
        ValidationError: If the input data is invalid, from the Project.clean() validation.
    """

    class Arguments:
        input = CreateProjectInput(required=True)

    project = graphene.Field(lambda: ProjectType)

    @login_required
    def mutate(self, info, input):
        """Create a new project in the database with the given input field data."""
        project = Project.objects.create(**input)
        return CreateProject(project=project)


class UpdateProject(graphene.Mutation):
    """Mutation for updating an existing project.

    Arguments:
        id (ID): The ID of the project to update.
        input (PartialUpdateProjectInput): Input object containing the fields to update.

    Fields:
        project (ProjectType): The updated project object.

    Methods:
        mutate():
            Validates and updates the project in the database with the given input field data.

    Returns:
        UpdateProject: An instance of the mutation class containing the updated project as a field.

    Raises:
        PermissionDenied: If the query/user is not authenticated.
        Project.DoesNotExist: If the project with the specified ID does not exist.
        ValidationError: If the input data is invalid, from the Project.clean() validation.
    """

    class Arguments:
        id = graphene.ID(required=True)
        input = PartialUpdateProjectInput(required=True)

    project = graphene.Field(lambda: ProjectType)

    @login_required
    def mutate(self, info, id, input):
        """Validates and updates the project in the database with the given input field data."""
        project = Project.objects.get(pk=id)
        for attr, value in input.items():
            setattr(project, attr, value)
        project.full_clean()
        project.save(update_fields=input.keys())
        return UpdateProject(project=project)


class DeleteProject(graphene.Mutation):
    """Mutation for deleting an existing project.

    Arguments:
        id (ID): The ID of the project to delete.

    Fields:
        success (bool): Indicates whether the deletion was successful.

    Methods:
        mutate():
            Deletes the project from the database.

    Returns:
        DeleteItem: An instance of the mutation class containing the success flag as a field.

    Raises:
        PermissionDenied: If the query/user is not authenticated.
        Project.DoesNotExist: If the project with the specified ID does not exist.
    """

    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @login_required
    def mutate(self, info, id):
        """Deletes the project from the database."""
        project = Project.objects.get(pk=id)
        project.delete()
        return DeleteProject(success=True)


class CreateItem(graphene.Mutation):
    """Mutation for creating a new item.

    Arguments:
        input (CreateItemInput): Input object containing the details of the item to create.

    Fields:
        item (ItemType): The newly created item object.

    Methods:
        mutate():
            Create a new item in the database with the given input field data.

    Returns:
        CreateItem: An instance of the mutation class containing the created item as a field.

    Raises:
        PermissionDenied: If the query/user is not authenticated.
        Project.DoesNotExist: If the specified project ID does not exist.
        Item.DoesNotExist: If the specified parent item ID does not exist.
        ValidationError: If the input data is invalid, from the Item.clean() validation.
    """

    class Arguments:
        input = CreateItemInput(required=True)

    item = graphene.Field(lambda: ItemType)

    @login_required
    def mutate(self, info, input):
        """Create a new item in the database with the given input field data."""
        # Get the project instance (returns error message id is not found)
        project_id = input.pop("project", None)
        project = Project.objects.get(pk=project_id) if project_id else None

        # Get the parent instance if it's defined (returns error message if id is not found)
        parent_id = input.pop("parent", None)
        parent = Item.objects.get(pk=parent_id) if parent_id else None

        # Get the item type instance if it's defined (returns error message if id is not found)
        item_type_id = input.pop("item_type", None)
        item_type = ItemTypeOption.objects.get(pk=item_type_id) if item_type_id else None

        # Get the item_status instance if it's defined (returns error message if id is not found)
        item_status_id = input.pop("item_status", None)
        item_status = ItemStatusOption.objects.get(pk=item_status_id) if item_status_id else None

        # Get the item_priority instance if it's defined (returns error message if id is not found)
        item_priority_id = input.pop("item_priority", None)
        item_priority = ItemPriorityOption.objects.get(pk=item_priority_id) if item_priority_id else None

        item = Item.objects.create(project=project, parent=parent, item_type=item_type, item_status=item_status, item_priority=item_priority, **input)
        return CreateItem(item=item)


class UpdateItem(graphene.Mutation):
    """Mutation for updating an existing item.

    Arguments:
        id (ID): The ID of the item to update.
        input (PartialUpdateItemInput): An input object containing the fields to update.

    Fields:
        item (ItemType): The updated item object.

    Methods:
        mutate():
            Validates and updates the item in the database with the given input field data.

    Returns:
        UpdateItem: An instance of the mutation class containing the updated item as a field.

    Raises:
        PermissionDenied: If the query/user is not authenticated.
        Item.DoesNotExist: If the item with the specified ID does not exist.
        Project.DoesNotExist: If the project with the specified ID does not exist.
        Item.DoesNotExist: If the parent item with the specified ID does not exist.
        ValidationError: If the input data is invalid, from the Item.clean() validation.
    """

    class Arguments:
        id = graphene.ID(required=True)
        input = PartialUpdateItemInput(required=True)

    item = graphene.Field(lambda: ItemType)

    @login_required
    def mutate(self, info, id, input):
        """Validates and updates the item in the database with the given input field data."""
        fields_to_update = input.keys()
        item = Item.objects.get(pk=id)

        # Update the project using the project instance if it's given (returns error message if id is not found)
        project_id = input.pop("project", None)
        if project_id:
            item.project = Project.objects.get(pk=project_id)

        # Update the parent using the parent instance if it's given (returns error message if id is not found)
        parent_id = input.pop("parent", None)
        if parent_id:
            item.parent = Item.objects.get(pk=parent_id)

        # Update the item_type using the item_type instance if it's given (returns error message if id is not found)
        item_type_id = input.pop("item_type", None)
        if item_type_id:
            item.item_type = ItemTypeOption.objects.get(pk=item_type_id)

        # Update the item_status using the item_status instance if it's given (returns error message if id is not found)
        item_status_id = input.pop("item_status", None)
        if item_status_id:
            item.item_status = ItemStatusOption.objects.get(pk=item_status_id)

        # Update the item_priority using the item_priority instance if it's given (returns error message if id is not found)
        item_priority_id = input.pop("item_priority", None)
        if item_priority_id:
            item.item_priority = ItemPriorityOption.objects.get(pk=item_priority_id)

        for attr, value in input.items():
            setattr(item, attr, value)
        item.full_clean()
        item.save(update_fields=fields_to_update)
        return UpdateItem(item=item)


class DeleteItem(graphene.Mutation):
    """Mutation for deleting an existing item.

    Arguments:
        id (ID): The ID of the item to delete.

    Fields:
        success (bool): Indicates whether the deletion was successful.

    Methods:
        mutate():
            Deletes the item from the database.

    Returns:
        DeleteItem: An instance of the mutation class containing the success flag as a field.

    Raises:
        PermissionDenied: If the query/user is not authenticated.
        Project.DoesNotExist: If the item with the specified ID does not exist.
    """

    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @login_required
    def mutate(self, info, id):
        """Deletes the item from the database."""
        item = Item.objects.get(pk=id)
        item.delete()
        return DeleteItem(success=True)


class Mutation(graphene.ObjectType):
    """GraphQL Mutation definition for the Organiser app.

    Fields:
        create_project (CreateProject): Mutation for creating a new project.
        update_project (UpdateProject): Mutation for updating an existing project.
        delete_project (DeleteProject): Mutation for deleting an existing project.
        create_item (CreateItem): Mutation for creating a new item.
        update_item (UpdateItem): Mutation for updating an existing item.
        delete_item (DeleteItem): Mutation for deleting an existing item.
    """

    create_project = CreateProject.Field()
    update_project = UpdateProject.Field()
    delete_project = DeleteProject.Field()
    create_item = CreateItem.Field()
    update_item = UpdateItem.Field()
    delete_item = DeleteItem.Field()
