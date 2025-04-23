from app.models import User
from app.schemas import UserBase, UserCreate, UserRead, UserUpdate


def get_model_fields(model):
    return {col.name for col in model.__table__.columns}


def get_schema_fields(schema):
    return set(schema.model_fields.keys())


def test_user_schema_matches_model():
    """The User schemas must not contain any fields that do not exist in the User model"""
    model_fields = get_model_fields(User)
    total_schema_fields = set().union(
        get_schema_fields(UserBase),
        get_schema_fields(UserCreate),
        get_schema_fields(UserRead),
        get_schema_fields(UserUpdate),
    )
    assert total_schema_fields.issubset(
        model_fields
    ), f"User schema field(s) {total_schema_fields - model_fields} not found in model"
