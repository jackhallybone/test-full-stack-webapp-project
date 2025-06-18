import graphene

from items.graphql.crud import BaseCRUD
from items.graphql.inputs import (
    CreateItemInput,
    CreateItemLocationInput,
    CreateItemStatusInput,
    CreateItemTypeInput,
    CreateProjectInput,
    UpdateItemInput,
    UpdateItemLocationInput,
    UpdateItemStatusInput,
    UpdateItemTypeInput,
    UpdateProjectInput,
)
from items.graphql.types import ItemLocationType, ItemStatusType
from items.graphql.types import ItemType as ItemGraphQLType
from items.graphql.types import ItemTypeType, ProjectType
from items.models import Item, ItemLocation, ItemStatus, ItemType, Project


class CreateProject(graphene.Mutation):
    class Arguments:
        input = CreateProjectInput(required=True)

    project = graphene.Field(lambda: ProjectType)

    @classmethod
    def mutate(cls, root, info, input):
        project = BaseCRUD(Project).create(input)
        return CreateProject(project=project)


class UpdateProject(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        input = UpdateProjectInput(required=True)

    project = graphene.Field(lambda: ProjectType)

    @classmethod
    def mutate(cls, root, info, id, input):
        project = BaseCRUD(Project).update(id, input)
        return UpdateProject(project=project)


class DeleteProject(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()
    project = graphene.Field(lambda: ProjectType)

    @classmethod
    def mutate(cls, root, info, id):
        project = BaseCRUD(Project).delete(id)
        return DeleteProject(success=True, project=project)


class CreateItemType(graphene.Mutation):
    class Arguments:
        input = CreateItemTypeInput(required=True)

    item_type = graphene.Field(lambda: ItemTypeType)

    @classmethod
    def mutate(cls, root, info, input):
        item_type = BaseCRUD(ItemType).create(input)
        return CreateItemType(item_type=item_type)


class UpdateItemType(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        input = UpdateItemTypeInput(required=True)

    item_type = graphene.Field(lambda: ItemTypeType)

    @classmethod
    def mutate(cls, root, info, id, input):
        item_type = BaseCRUD(ItemType).update(id, input)
        return UpdateItemType(item_type=item_type)


class DeleteItemType(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()
    item_type = graphene.Field(lambda: ItemTypeType)

    @classmethod
    def mutate(cls, root, info, id):
        item_type = BaseCRUD(ItemType).delete(id)
        return DeleteItemType(success=True, item_type=item_type)


class CreateItemStatus(graphene.Mutation):
    class Arguments:
        input = CreateItemStatusInput(required=True)

    item_status = graphene.Field(lambda: ItemStatusType)

    @classmethod
    def mutate(cls, root, info, input):
        item_status = BaseCRUD(ItemStatus).create(input)
        return CreateItemStatus(item_status=item_status)


class UpdateItemStatus(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        input = UpdateItemStatusInput(required=True)

    item_status = graphene.Field(lambda: ItemStatusType)

    @classmethod
    def mutate(cls, root, info, id, input):
        item_status = BaseCRUD(ItemStatus).update(id, input)
        return UpdateItemStatus(item_status=item_status)


class DeleteItemStatus(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()
    item_status = graphene.Field(lambda: ItemStatusType)

    @classmethod
    def mutate(cls, root, info, id):
        item_status = BaseCRUD(ItemStatus).delete(id)
        return DeleteItemStatus(success=True, item_status=item_status)


class CreateItemLocation(graphene.Mutation):
    class Arguments:
        input = CreateItemLocationInput(required=True)

    item_location = graphene.Field(lambda: ItemLocationType)

    @classmethod
    def mutate(cls, root, info, input):
        item_location = BaseCRUD(ItemLocation).create(input)
        return CreateItemLocation(item_location=item_location)


class UpdateItemLocation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        input = UpdateItemLocationInput(required=True)

    item_location = graphene.Field(lambda: ItemLocationType)

    @classmethod
    def mutate(cls, root, info, id, input):
        item_location = BaseCRUD(ItemLocation).update(id, input)
        return UpdateItemLocation(item_location=item_location)


class DeleteItemLocation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()
    item_location = graphene.Field(lambda: ItemLocationType)

    @classmethod
    def mutate(cls, root, info, id):
        item_location = BaseCRUD(ItemLocation).delete(id)
        return DeleteItemLocation(success=True, item_location=item_location)


class CreateItem(graphene.Mutation):
    class Arguments:
        input = CreateItemInput(required=True)

    item = graphene.Field(lambda: ItemGraphQLType)

    @classmethod
    def mutate(cls, root, info, input):
        item = BaseCRUD(Item).create(input)
        return CreateItem(item=item)


class UpdateItem(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        input = UpdateItemInput(required=True)

    item = graphene.Field(lambda: ItemGraphQLType)

    @classmethod
    def mutate(cls, root, info, id, input):
        item = BaseCRUD(Item).update(id, input)
        return UpdateItem(item=item)


class DeleteItem(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()
    item = graphene.Field(lambda: ItemGraphQLType)

    @classmethod
    def mutate(cls, root, info, id):
        item = BaseCRUD(Item).delete(id)
        return DeleteItem(success=True, item=item)


class Mutation(graphene.ObjectType):
    create_project = CreateProject.Field()
    update_project = UpdateProject.Field()
    delete_project = DeleteProject.Field()
    create_item_type = CreateItemType.Field()
    update_item_type = UpdateItemType.Field()
    delete_item_type = DeleteItemType.Field()
    create_item_status = CreateItemStatus.Field()
    update_item_status = UpdateItemStatus.Field()
    delete_item_status = DeleteItemStatus.Field()
    create_item_location = CreateItemLocation.Field()
    update_item_location = UpdateItemLocation.Field()
    delete_item_location = DeleteItemLocation.Field()
    create_item = CreateItem.Field()
    update_item = UpdateItem.Field()
    delete_item = DeleteItem.Field()
