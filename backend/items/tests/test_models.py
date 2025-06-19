import pytest
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save

from items.models import Item, ItemLocation, ItemStatus, ItemType, Project
from items.signals import create_default_item_attributes

## Fixtures


@pytest.fixture
def clean_project():
    """Create a project without triggering default item attribute creation."""
    post_save.disconnect(create_default_item_attributes, sender=Project)
    project = Project.objects.create(name="project")
    post_save.connect(create_default_item_attributes, sender=Project)
    return project


@pytest.fixture
def example_hierarchy(clean_project):
    """Create an example hierarchy.

    project
        item_1
            item_2
                item_3
    other_project
        other_item
    """
    project = clean_project
    # Create some item attributes
    area = ItemType.objects.create(
        project=project, name="area", default=False, order=1, nestable=False
    )
    task = ItemType.objects.create(
        project=project, name="task", default=True, order=2, nestable=True
    )
    todo = ItemStatus.objects.create(
        project=project, name="todo", default=True, order=1
    )
    done = ItemStatus.objects.create(
        project=project, name="done", default=False, order=2
    )
    backlog = ItemLocation.objects.create(
        project=project, name="backlog", default=True, order=1
    )
    cleared = ItemLocation.objects.create(
        project=project, name="cleared", default=False, order=2
    )
    # Create some items
    item_1 = Item.objects.create(
        project=project,
        item_type=area,
        item_status=todo,
        item_location=backlog,
        title="item_1",
        changelog="item_1",
    )
    item_2 = Item.objects.create(
        project=project,
        parent=item_1,
        item_type=task,
        item_status=todo,
        item_location=backlog,
        title="item_2",
    )
    item_3 = Item.objects.create(
        project=project,
        parent=item_2,
        item_type=task,
        item_status=done,
        item_location=cleared,
        title="item_3",
    )
    # Create a second project with an item, using default attributes
    other_project = Project.objects.create(name="other_project")
    other_item = Item.objects.create(
        project=other_project,
        item_type=other_project.get_default_item_type(),
        item_status=other_project.get_default_item_status(),
        item_location=other_project.get_default_item_location(),
        title="other_item",
    )
    return project, item_1, item_2, item_3, other_project, other_item


#### Filters


@pytest.mark.django_db
def test_project_filter_no_filters(example_hierarchy):
    """Verify that running the project filter with no filters/options returns the original QuerySet."""
    qs = Project.objects.all()
    assert list(qs.filter_projects()) == list(qs)


@pytest.mark.django_db
def test_project_filter_name_contains(example_hierarchy):
    """Verify filtering for project name field."""
    _, _, _, _, other_project, _ = example_hierarchy
    assert set(Project.objects.all().filter_projects(name_contains="OTHER")) == {
        other_project
    }
    assert (
        Project.objects.all().filter_projects(name_contains="not in any names").count()
        == 0
    )


@pytest.mark.django_db
def test_item_filter_no_filters(example_hierarchy):
    """Verify that running the item filter with no filters/options returns the original QuerySet."""
    qs = Item.objects.all()
    assert list(qs.filter_items()) == list(qs)


@pytest.mark.django_db
def test_item_filter_title_contains(example_hierarchy):
    """Verify filtering for item title field."""
    _, item_1, _, _, _, _ = example_hierarchy
    assert set(Item.objects.all().filter_items(title_contains="_1")) == {item_1}
    assert (
        Item.objects.all().filter_items(title_contains="not in any titles").count() == 0
    )


@pytest.mark.django_db
def test_item_filter_changelog_contains(example_hierarchy):
    """Verify filtering for item changelog field."""
    _, item_1, _, _, _, _ = example_hierarchy
    assert set(Item.objects.all().filter_items(changelog_contains="_1")) == {item_1}
    assert (
        Item.objects.all()
        .filter_items(changelog_contains="not in any changelogs")
        .count()
        == 0
    )


@pytest.mark.django_db
def test_item_filter_project(example_hierarchy):
    """Verify filtering for item project field."""
    project, item_1, item_2, item_3, _, _ = example_hierarchy
    assert set(Item.objects.all().filter_items(project=project.id)) == {
        item_1,
        item_2,
        item_3,
    }
    assert Item.objects.all().filter_items(project=1000).count() == 0


@pytest.mark.django_db
def test_item_filter_item_type(example_hierarchy):
    """Verify filtering for item type attribute field."""
    project, _, item_2, item_3, _, _ = example_hierarchy
    task = project.get_default_item_type()
    assert set(Item.objects.all().filter_items(item_type=task.id)) == {item_2, item_3}
    assert Item.objects.all().filter_items(item_type=1000).count() == 0


@pytest.mark.django_db
def test_item_filter_item_status(example_hierarchy):
    """Verify filtering for item status attribute field."""
    project, item_1, item_2, _, _, _ = example_hierarchy
    todo = project.get_default_item_status()
    assert set(Item.objects.all().filter_items(item_status=todo.id)) == {item_1, item_2}
    assert Item.objects.all().filter_items(item_status=1000).count() == 0


@pytest.mark.django_db
def test_item_filter_item_location(example_hierarchy):
    """Verify filtering for item location attribute field."""
    project, item_1, item_2, _, _, _ = example_hierarchy
    backlog = project.get_default_item_location()
    assert set(Item.objects.all().filter_items(item_location=backlog.id)) == {
        item_1,
        item_2,
    }
    assert Item.objects.all().filter_items(item_location=1000).count() == 0


#### Project


@pytest.mark.django_db
def test_project_ordering():
    """Verify that `Project`s are ordered alphanumerically by name."""
    beta = Project.objects.create(name="beta")
    alpha = Project.objects.create(name="alpha")
    assert list(Project.objects.all()) == [alpha, beta]


@pytest.mark.django_db
@pytest.mark.parametrize(
    "model, getter_name",
    [
        (ItemType, "get_item_types"),
        (ItemStatus, "get_item_statuses"),
        (ItemLocation, "get_item_locations"),
    ],
)
def test_project_get_item_attributes(clean_project, model, getter_name):
    """Verify that a `Project` can list all the item attributes assigned to it."""
    getter_func = getattr(clean_project, getter_name)
    assert not getter_func().exists()

    model.objects.create(project=clean_project, name="new", order=1)
    assert getter_func().count() == 1


@pytest.mark.django_db
@pytest.mark.parametrize(
    "model, getter_name",
    [
        (ItemType, "get_default_item_type"),
        (ItemStatus, "get_default_item_status"),
        (ItemLocation, "get_default_item_location"),
    ],
)
def test_project_get_default_item_attribute(clean_project, model, getter_name):
    """Verify that a `Project` can find the default item attribute assigned to it."""
    getter_func = getattr(clean_project, getter_name)
    assert getter_func() == None

    default = model.objects.create(
        project=clean_project, name="test", order=1, default=True
    )
    assert getter_func() == default


@pytest.mark.django_db
def test_project_get_descendants(example_hierarchy):
    """Verify that a `Project` can list all its descendants."""
    project, item_1, item_2, item_3, _, _ = example_hierarchy
    assert list(project.get_descendants()) == [item_1, item_2, item_3]


@pytest.mark.django_db
def test_project_get_num_descendants(example_hierarchy):
    """Verify that a `Project` can count all its descendants."""
    project, _, _, _, _, _ = example_hierarchy
    assert project.get_num_descendants() == 3


@pytest.mark.django_db
def test_project_get_children(example_hierarchy):
    """Verify that a `Project` can list all its children."""
    project, item_1, _, _, _, _ = example_hierarchy
    assert list(project.get_children()) == [item_1]


@pytest.mark.django_db
def test_project_get_num_children(example_hierarchy):
    """Verify that a `Project` can count all its children."""
    project, _, _, _, _, _ = example_hierarchy
    assert project.get_num_children() == 1


@pytest.mark.django_db
def test_project_clean_name():
    """Verify that `Project` names are stripped of whitespace and cannot be empty."""
    valid = Project.objects.create(name=" test ")
    assert valid.name == "test"
    with pytest.raises(ValidationError):
        Project.objects.create(name="  ")


#### Item Attributes (ItemType, ItemStatus, ItemLocation)

itemattribute_models = [ItemType, ItemStatus, ItemLocation]


@pytest.mark.django_db
@pytest.mark.parametrize("model", itemattribute_models)
def test_itemattribute_ordering(clean_project, model):
    """Verify that item attributes are ordered by their order field."""
    three = model.objects.create(project=clean_project, name="three", order=3)
    two = model.objects.create(project=clean_project, name="two", order=2)
    one = model.objects.create(project=clean_project, name="one", order=1)
    assert list(model.objects.all()) == [one, two, three]


@pytest.mark.django_db
@pytest.mark.parametrize("model", itemattribute_models)
def test_itemattribute_clean_name(clean_project, model):
    """Verify that item attribute names are stripped of whitespace and cannot be empty."""
    valid = model.objects.create(project=clean_project, name=" test ", order=1)
    assert valid.name == "test"
    with pytest.raises(ValidationError):
        model.objects.create(project=clean_project, name="  ", order=1)


@pytest.mark.django_db
@pytest.mark.parametrize("model", itemattribute_models)
def test_itemattribute_clean_unique_name(clean_project, model):
    """Verify that item attributes of the same type must have unique names within a `Project`."""
    model.objects.create(project=clean_project, name="name", order=1)
    with pytest.raises(ValidationError):
        model.objects.create(project=clean_project, name="name", order=2)


@pytest.mark.django_db
@pytest.mark.parametrize("model", itemattribute_models)
def test_itemattribute_clean_one_default(clean_project, model):
    """Verify that each item attribute type can only have one default option within a `Project`."""
    model.objects.create(project=clean_project, name="first", default=True, order=1)
    with pytest.raises(ValidationError):
        model.objects.create(
            project=clean_project, name="second", default=True, order=2
        )


@pytest.mark.django_db
@pytest.mark.parametrize("model", itemattribute_models)
def test_itemattribute_clean_unique_order(clean_project, model):
    """Verify that the ordering of item attribute is unique with type within a `Project`."""
    model.objects.create(project=clean_project, name="first", order=1)
    with pytest.raises(ValidationError):
        model.objects.create(project=clean_project, name="second", order=1)


#### Item


@pytest.mark.django_db
def test_item_ordering(clean_project):
    """Verify that `Item`s are ordered alphanumerically by name."""
    # Create some item attributes
    second = ItemType.objects.create(project=clean_project, name="second", order=2)
    first = ItemType.objects.create(project=clean_project, name="first", order=1)
    status = ItemStatus.objects.create(project=clean_project, name="status", order=1)
    location = ItemLocation.objects.create(
        project=clean_project, name="location", order=1
    )
    # Create some items out of order
    one = Item.objects.create(
        project=clean_project,
        item_type=second,
        item_status=status,
        item_location=location,
        title="one",
    )
    two = Item.objects.create(
        project=clean_project,
        item_type=first,
        item_status=status,
        item_location=location,
        title="two",
    )
    three = Item.objects.create(
        project=clean_project,
        item_type=first,
        item_status=status,
        item_location=location,
        title="three",
    )
    assert list(Item.objects.all()) == [two, three, one]


@pytest.mark.django_db
def test_item_get_ancestors(example_hierarchy):
    """Verify that an `Item` can list all its ancestors."""
    _, item_1, item_2, item_3, _, _ = example_hierarchy
    assert list(item_3.get_ancestors()) == [item_1, item_2]


@pytest.mark.django_db
def test_item_get_num_ancestors(example_hierarchy):
    """Verify that an `Item` can count all its ancestors."""
    _, _, _, item_3, _, _ = example_hierarchy
    assert item_3.get_num_ancestors() == 2


@pytest.mark.django_db
def test_item_get_descendants(example_hierarchy):
    """Verify that an `Item` can list all its descendants."""
    _, item_1, item_2, item_3, _, _ = example_hierarchy
    assert list(item_1.get_descendants()) == [item_2, item_3]


@pytest.mark.django_db
def test_item_get_num_descendants(example_hierarchy):
    """Verify that an `Item` can count all its descendants."""
    _, item_1, _, _, _, _ = example_hierarchy
    assert item_1.get_num_descendants() == 2


@pytest.mark.django_db
def test_item_get_children(example_hierarchy):
    """Verify that an `Item` can list all its children."""
    _, item_1, item_2, _, _, _ = example_hierarchy
    assert list(item_1.get_children()) == [item_2]


@pytest.mark.django_db
def test_item_get_num_children(example_hierarchy):
    """Verify that an `Item` can count all its children."""
    _, item_1, _, _, _, _ = example_hierarchy
    assert item_1.get_num_children() == 1


@pytest.mark.django_db
def test_item_clean_title_and_changelog(example_hierarchy):
    """Verify that `Item` title and changelog are stripped of whitespace and title cannot be empty."""
    _, item_1, _, _, _, _ = example_hierarchy
    item_1.title = " test "
    item_1.changelog = " test "
    item_1.clean()
    assert (item_1.title == "test") and (item_1.changelog == "test")
    with pytest.raises(ValidationError):
        item_1.title = "  "
        item_1.clean()


@pytest.mark.django_db
def test_item_clean_crossing_project(example_hierarchy):
    """Verify that an `Item` cannot change project once created."""
    _, item_1, _, _, other_project, _ = example_hierarchy
    with pytest.raises(ValidationError):
        item_1.project = other_project
        item_1.clean()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "field_name, getter_name",
    [
        ("item_type", "get_default_item_type"),
        ("item_status", "get_default_item_status"),
        ("item_location", "get_default_item_location"),
    ],
)
def test_item_clean_attributes_crossing_project(
    example_hierarchy, field_name, getter_name
):
    """Verify that an `Item` cannot be assigned an attribute from another project."""
    _, item_1, _, _, other_project, _ = example_hierarchy
    with pytest.raises(ValidationError):
        setattr(item_1, field_name, getattr(other_project, getter_name)())
        item_1.clean()


@pytest.mark.django_db
def test_item_clean_own_parent(example_hierarchy):
    """Verify that an `Item` cannot be its own parent."""
    _, item_1, _, _, _, _ = example_hierarchy
    with pytest.raises(ValidationError):
        item_1.parent = item_1
        item_1.clean()


@pytest.mark.django_db
def test_item_clean_same_project_as_parent(example_hierarchy):
    """Verify that an `Item` must belong to the same project as its parent."""
    _, item_1, _, _, _, other_item = example_hierarchy
    with pytest.raises(ValidationError):
        item_1.parent = other_item
        item_1.clean()


@pytest.mark.django_db
def test_item_clean_circular_ancestry(example_hierarchy):
    """Verify that an `Item` cannot be its own ancestor."""
    _, item_1, _, item_3, _, _ = example_hierarchy
    with pytest.raises(ValidationError):
        item_1.parent = item_3  # item_1>item_2>item_3>item_1...
        item_1.clean()


@pytest.mark.django_db
def test_item_clean_nestable_type():
    """Verify that only nestable `ItemType`s can nest."""
    project = Project.objects.create(name="project")
    nestable = ItemType.objects.create(
        project=project, name="nestable", order=10, nestable=True
    )
    not_nestable = ItemType.objects.create(
        project=project, name="not_nestable", order=11, nestable=False
    )
    parent = Item.objects.create(
        project=project,
        item_type=nestable,
        item_status=project.get_default_item_status(),
        item_location=project.get_default_item_location(),
        title="parent",
    )
    Item.objects.create(
        project=project,
        parent=parent,
        item_type=nestable,
        item_status=project.get_default_item_status(),
        item_location=project.get_default_item_location(),
        title="child",
    )
    with pytest.raises(ValidationError):
        parent = Item.objects.create(
            project=project,
            item_type=not_nestable,
            item_status=project.get_default_item_status(),
            item_location=project.get_default_item_location(),
            title="parent",
        )
        Item.objects.create(
            project=project,
            parent=parent,
            item_type=not_nestable,
            item_status=project.get_default_item_status(),
            item_location=project.get_default_item_location(),
            title="child",
        )


@pytest.mark.django_db
def test_item_clean_order():
    """Verify that non-nestable `ItemType`s must follow their order when nesting."""
    project = Project.objects.create(name="project")
    above = ItemType.objects.create(
        project=project, name="nestable", order=10, nestable=False
    )
    below = ItemType.objects.create(
        project=project, name="not_nestable", order=11, nestable=False
    )
    parent = Item.objects.create(
        project=project,
        item_type=above,
        item_status=project.get_default_item_status(),
        item_location=project.get_default_item_location(),
        title="parent",
    )
    Item.objects.create(
        project=project,
        parent=parent,
        item_type=below,
        item_status=project.get_default_item_status(),
        item_location=project.get_default_item_location(),
        title="child",
    )
    with pytest.raises(ValidationError):
        parent = Item.objects.create(
            project=project,
            item_type=below,
            item_status=project.get_default_item_status(),
            item_location=project.get_default_item_location(),
            title="parent",
        )
        Item.objects.create(
            project=project,
            parent=parent,
            item_type=above,
            item_status=project.get_default_item_status(),
            item_location=project.get_default_item_location(),
            title="child",
        )


@pytest.mark.django_db
def test_item_hierarchy_depth(clean_project, num_levels=100):
    """Verify that we can create and fetch on a nested hierarchy deeper than reasonably expected."""
    nestable = ItemType.objects.create(
        project=clean_project, name="type", order=1, nestable=True
    )
    status = ItemStatus.objects.create(project=clean_project, name="status", order=1)
    location = ItemLocation.objects.create(
        project=clean_project, name="location", order=1
    )
    first_parent = Item.objects.create(
        project=clean_project,
        item_type=nestable,
        item_status=status,
        item_location=location,
        title="parent",
    )
    parent = first_parent
    for i in range(num_levels):
        child = Item.objects.create(
            project=clean_project,
            parent=parent,
            item_type=nestable,
            item_status=status,
            item_location=location,
            title=f"child {i}",
        )
        parent = child
    assert first_parent.get_num_descendants() == num_levels
    assert child.get_num_ancestors() == num_levels
