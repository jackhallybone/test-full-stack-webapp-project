import graphene


class ProjectFilterInput(graphene.InputObjectType):
    name_contains = graphene.String()


class ItemFilterInput(graphene.InputObjectType):
    title_contains = graphene.String()
    changelog_contains = graphene.String()
    project = graphene.ID()
    item_type = graphene.ID()
    item_status = graphene.ID()
    item_location = graphene.ID()


class CreateProjectInput(graphene.InputObjectType):
    name = graphene.String(required=True)


class UpdateProjectInput(graphene.InputObjectType):
    name = graphene.String()


class BaseCreateItemAttributeInput(graphene.InputObjectType):
    project = graphene.ID(required=True)
    name = graphene.String(required=True)
    default = graphene.Boolean()
    order = graphene.Int(required=True)


class BaseUpdateItemAttributeInput(graphene.InputObjectType):
    name = graphene.String()
    default = graphene.Boolean()
    order = graphene.Int()


class CreateItemTypeInput(BaseCreateItemAttributeInput):
    nestable = graphene.Boolean()


class UpdateItemTypeInput(BaseUpdateItemAttributeInput):
    nestable = graphene.Boolean()


class CreateItemStatusInput(BaseCreateItemAttributeInput):
    pass


class UpdateItemStatusInput(BaseUpdateItemAttributeInput):
    pass


class CreateItemLocationInput(BaseCreateItemAttributeInput):
    pass


class UpdateItemLocationInput(BaseUpdateItemAttributeInput):
    pass


class CreateItemInput(graphene.InputObjectType):
    project = graphene.ID(required=True)
    parent = graphene.ID()
    item_type = graphene.ID(required=True)
    item_status = graphene.ID(required=True)
    item_location = graphene.ID(required=True)
    title = graphene.String(required=True)
    changelog = graphene.String()
    requirements = graphene.String()
    outcome = graphene.String()


class UpdateItemInput(graphene.InputObjectType):
    parent = graphene.ID()
    item_type = graphene.ID()
    item_status = graphene.ID()
    item_location = graphene.ID()
    title = graphene.String()
    changelog = graphene.String()
    requirements = graphene.String()
    outcome = graphene.String()
