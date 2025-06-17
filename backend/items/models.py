from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from items.mixins import AuditMixin

class Project(AuditMixin):
    """The model representing a project in the hierarchical system.

    Inherits from `AuditMixin`.

    Attributes:
        name (str): The name of the project.
    """

    name = models.CharField(max_length=100)

    class Meta:
        ordering = ["name"]  # order queries alphanumerically (numbers then A-Z)

    def __str__(self):
        return f"Project: {self.name}"

    def get_default_item_type(self):
        """Return the `ItemType` marked as default for the current `Project`."""
        return self.itemtype_set.filter(default=True).first()

    def get_default_item_status(self):
        """Return the `ItemStatus` marked as default for the current `Project`."""
        return self.itemstatus_set.filter(default=True).first()

    def get_default_item_location(self):
        """Return the `ItemLocation` marked as default for the current `Project`."""
        return self.itemlocation_set.filter(default=True).first()

    def get_descendants(self):
        """Return a QuerySet of all `Item`s that are descendants of (assigned to) this `Project`."""
        return self.items.all()

    def get_num_descendants(self):
        """Return the number of `Item`s that are descendants of (assigned to) this `Project`."""
        return self.get_descendants().count()

    def get_children(self):
        """Return a QuerySet of `Item`s that are direct children (do not have a parent `Item`) of this `Project`."""
        return self.items.filter(parent=None)

    def get_num_children(self):
        """Return the number of `Item`s that are direct children (do not have a parent `Item`) of this `Project`."""
        return self.get_children().count()

    def clean(self):
        """Validate the model data before saving."""
        super().clean()

        self.name = self.name.strip()  # Strip whitespace

        if not self.name:
            raise ValidationError(f"{self.__class__.__name__} name cannot be blank.")

    def save(self, *args, **kwargs):
        """Calls the overloaded `clean` method before saving."""
        self.clean()
        super().save(*args, **kwargs)


class BaseItemAttribute(models.Model):
    """An abstract model containing the common elements of the attributes an `Item` can have.

    Attributes:
        project (Project): The project that the attribute belongs to.
        name (str): The name of the attribute.
        default (bool): A flag to indicate if this is the default attribute it its set. Defaults to False.
        order (int): The number of the attribute in the logical order of its set.
    """

    project = models.ForeignKey(Project, on_delete=models.CASCADE) # uses default related_name
    name = models.CharField(max_length=100)
    default = models.BooleanField(default=False)
    order = models.SmallIntegerField()

    class Meta:
        abstract = True
        ordering = ["order"] # ascending

    def __str__(self):
        return f"{self.__class__.__name__}: {self.name} (for {self.project.name})"

    def clean(self):
        """Validate the model data before saving."""
        super().clean()

        self.name = self.name.strip()  # Strip whitespace

        if not self.name:
            raise ValidationError(f"{self.__class__.__name__} name cannot be blank.")

        if type(self).objects.filter(project=self.project, name=self.name).exclude(id=self.id).exists():
            raise ValidationError(_(f"{self.__class__.__name__} names must be unique within each project."))

        if self.default:
            if type(self).objects.filter(project=self.project, default=True).exclude(id=self.id).exists():
                raise ValidationError(_(f"There can only be one default {self.__class__.__name__} within each project."))

        if type(self).objects.filter(project=self.project, order=self.order).exclude(id=self.id).exists():
            raise ValidationError(_(f"{self.__class__.__name__} order must be unique within each project."))

    def save(self, *args, **kwargs):
        """Calls the `clean` method before saving the item."""
        self.clean()
        super().save(*args, **kwargs)


class ItemType(BaseItemAttribute):
    """A model representing the type attribute of items in the hierarchical system.

    Projects contains a set of type attributes which can be assigned to items belonging to that project.

    Inherits from `BaseItemAttribute`.

    Attributes:
        nestable (bool): A flag to indicate if items of this type can nest below items of the same type. Defaults to False.
    """
    nestable = models.BooleanField(default=False)

    @staticmethod
    def default_options():
        """Return a list of default item type attributes for when creating a new project."""
        return [
            {'name': _('Area'), 'default': False, 'order': 1, 'nestable': False},
            {'name': _('Epic'), 'default': False, 'order': 2, 'nestable': False},
            {'name': _('Feature'), 'default': False, 'order': 3, 'nestable': False},
            {'name': _('Task'), 'default': True, 'order': 4, 'nestable': True},
        ]


class ItemStatus(BaseItemAttribute):
    """A model representing the status attribute of items in the hierarchical system.

    Projects contains a set of status attributes which can be assigned to items belonging to that project.

    Inherits from `BaseItemAttribute`.
    """

    @staticmethod
    def default_options():
        """Return a list of default item status attributes for when creating a new project."""
        return [
            {'name': _('To Do'), 'default': True, 'order': 1},
            {'name': _('In Progress'), 'default': False, 'order': 2},
            {'name': _('Done'), 'default': False, 'order': 3},
        ]


class ItemLocation(BaseItemAttribute):
    """A model representing the location attribute of items in the hierarchical system.

    Projects contains a set of location attributes which can be assigned to items belonging to that project.

    Inherits from `BaseItemAttribute`.
    """

    @staticmethod
    def default_options():
        """Return a list of default item location attributes for when creating a new project."""
        return [
            {'name': _('Backlog'), 'default': True, 'order': 1},
            {'name': _('Board'), 'default': False, 'order': 2},
            {'name': _('Cleared'), 'default': False, 'order': 3},
        ]


class Item(AuditMixin):
    """A model representing an item in the hierarchical system.

    Items belong to a project and may have hierarchical relationships with other items.

    Inherits from `AuditMixin`.

    Attributes:
        project (Project): The project that this item belongs to.
        parent (Item, optional): The item that this item is nested below.
        item_type (ItemType): The type attribute for this item.
        item_status (ItemStatus): The status attribute for this item.
        item_location (ItemLocation): The location attribute for this item.
        title (str): A summary of what needs to be done.
        changelog (str, optional): A summary of what has been done.
        requirements (str, optional): A description of what needs to be done.
        outcomes (str, optional): A description of what was done.
    """

    project = models.ForeignKey(Project, related_name="items", on_delete=models.CASCADE)
    parent = models.ForeignKey("self", blank=True, null=True, related_name="children", on_delete=models.CASCADE)
    item_type = models.ForeignKey(ItemType, related_name="items", on_delete=models.CASCADE)
    item_status = models.ForeignKey(ItemStatus, related_name="items", on_delete=models.CASCADE)
    item_location = models.ForeignKey(ItemLocation, related_name="items", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    changelog = models.CharField(max_length=100, blank=True)
    requirements = models.TextField(blank=True)
    outcome = models.TextField(blank=True)

    class Meta:
        ordering = ["item_type", "created_at"]  # order queries by type then oldest first

    def __str__(self):
        return f"Item: {self.title} ({self.item_type.name} in {self.project.name})"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_project = getattr(self, "project", None)

    def _find_ancestors(self):
        """Create a list of ids of all `Item`s that are ancestors of this `Item, ordered from root to this item's parent."""
        # Get all items in the current items project, but only the id and parent_id fields
        items = Item.objects.filter(project_id=self.project_id).values_list("id", "parent_id")

        # Build a child->parent relationship lookup in the format {item_id: parent_id, ...}
        parent_lookup = {item_id: parent_id for item_id, parent_id in items}

        ancestor_ids = []
        visited_ids = {self.id}
        current_id = self.parent_id

        # Follow the parent fields upwards for each ancestor until there is no parent
        while current_id:

            # Check for circular references (id already in the ancestors list)
            if current_id in visited_ids:
                raise ValidationError(_("An item cannot be its own ancestor."))

            ancestor_ids.append(current_id)
            visited_ids.add(current_id)

            # Move to the next ancestor using the lookup dictionary (use item_id to get parent_id)
            current_id = parent_lookup.get(current_id)

        ancestor_ids.reverse()

        return ancestor_ids

    def get_ancestors(self):
        """Returns a QuerySet of all `Item`s that are ancestors of this `Item, ordered from root to this item's parent."""
        ancestor_ids = self._find_ancestors()
        return Item.objects.filter(id__in=ancestor_ids)

    def get_num_ancestors(self):
        """Returns the number of `Item`s that are ancestors of this `Item`."""
        ancestor_ids = self._find_ancestors()
        return len(ancestor_ids)

    def _find_descendants(self):
        """Create a list of ids of all `Item`s that are descendants of this `Item."""
        # Fetch only the necessary fields for traversing the ancestry (id, parent_id) for all items in the current project
        items = Item.objects.filter(project_id=self.project_id).values_list("id", "parent_id")

        # Build a parent->children relationship lookup dictionary in the format {parent_id: [child_id, ...], ...}
        child_lookup = {}
        for item_id, parent_id in items:
            child_lookup.setdefault(parent_id, []).append(item_id)

        descendants_ids = []
        parent_ids_to_process = [self.id]

        # Traverse the hierarchy starting from this item's ID
        while parent_ids_to_process:
            parent_id = parent_ids_to_process.pop(0)  # First-in-first-out
            children_ids = child_lookup.get(parent_id, [])
            descendants_ids.extend(children_ids)
            parent_ids_to_process.extend(children_ids)

        return descendants_ids

    def get_descendants(self):
        """Returns a QuerySet of all `Item`s that are descendants of this `Item."""
        descendants_ids = self._find_descendants()
        return Item.objects.filter(id__in=descendants_ids)

    def get_num_descendants(self):
        """Returns the number of `Item`s that are descendants of this `Item`."""
        descendants_ids = self._find_descendants()
        return len(descendants_ids)

    def get_children(self):
        """Return a QuerySet of `Item`s that are direct children of this `Item`."""
        return self.children.all()

    def get_num_children(self):
        """Return the number of `Item`s that are direct children of this `Item`."""
        return self.get_children().count()

    def clean(self):
        """Validate the model data before saving."""
        super().clean()

        self.title = self.title.strip()  # Strip whitespace
        self.changelog = self.changelog.strip()  # Strip whitespace

        if not self.title:
            raise ValidationError(_(f"{self.__class__.__name__} title cannot be empty."))

        if self._original_project and self.project != self._original_project:
            raise ValidationError(_("An item cannot change project once created."))

        if self.item_type not in self.project.itemtype_set.all():
            raise ValidationError(_("Item type attribute selection must belong to the same project as the item."))

        if self.item_status not in self.project.itemstatus_set.all():
            raise ValidationError(_("Item status attribute selection must belong to the same project as the item."))

        if self.item_location not in self.project.itemlocation_set.all():
            raise ValidationError(_("Item location attribute selection must belong to the same project as the item."))

        if self.parent:
            if self == self.parent:
                raise ValidationError(_("An item cannot be its own parent."))

            if self.parent.project != self.project:
                raise ValidationError(_("An item must belong to the same project as its parent."))

            # Prevent circular references in the hierarchy by raising a ValidationError if self is found in the ancestors list
            self._find_ancestors()

            if self.item_type == self.parent.item_type:
                if self.item_type.nestable:
                    pass # Allow nesting of two of the same nestable types
                else:
                    raise ValidationError(_("An item cannot be the same type as its parent unless they are both of the same nestable type."))
            elif self.item_type.order <= self.parent.item_type.order:
                raise ValidationError(
                    _("An item must be 'below' its parent in the hierarchy unless they are of the same nestable type.")
                )

    def save(self, *args, **kwargs):
        """Calls the `clean` method before saving the item."""
        self.clean()
        super().save(*args, **kwargs)
