import strawberry


@strawberry.type
class DeleteResponseType:
    message: str


@strawberry.input
class UserCreateInput:
    name: str
    email: str
    username: str | None = None


@strawberry.type
class UserType:
    id: int
    name: str
    email: str
    username: str | None


@strawberry.input
class UserUpdateInput:
    name: str | None = None
    email: str | None = None
    username: str | None = None
