from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from organiser.mixins import AuditMixin


class Project(AuditMixin, models.Model):
    """The model representing a project in the hierarchical system.

    Inherits from the AuditMixin abstract class.

    Fields:
        name (str): The name of the project. Required.
        description (str): A description of the project. Defaults to an empty string.

    Methods:
        __str__():
            Returns a string representation of the project with its name in the format "Project: {name}"
        get_default_item_type():
            Get the ItemTypeOption object associated with this project that is set to default.
        get_default_item_status():
            Get the ItemStatusOption object associated with this project that is set to default.
        get_default_item_priority():
            Get the ItemPriorityOption object associated with this project that is set to default.
        get_descendants():
            Returns a QuerySet of all Item objects associated with this project.
        get_children():
            Returns a QuerySet of the Item objects associated with this project that do not have a parent Item.
        get_num_children():
            Returns the number of Item objects associated with this project that do not have a parent Item.
        clean():
            Validates the project's data before saving. Raises ValidationError if invalid data or logic is found.
        save():
            Calls the `clean` method before saving the project.
    """

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]  # order queries alphanumerically (numbers then A-Z)

    def __str__(self):
        """Returns a string representation of the project as it's name."""
        return self.name

    def get_default_item_type(self):
        """Get the ItemTypeOption object associated with this project that is set to default."""
        return self.item_types.filter(default=True).first()

    def get_default_item_status(self):
        """Get the ItemStatusOption object associated with this project that is set to default."""
        return self.item_statuses.filter(default=True).first()

    def get_default_item_priority(self):
        """Get the ItemPriorityOption object associated with this project that is set to default."""
        return self.item_priorities.filter(default=True).first()

    def get_descendants(self):
        """Returns a QuerySet of all Item objects associated with this project.

        By default the results will be ordered as defined in the Item model.
        """
        return self.items.all()

    def get_children(self):
        """Returns a QuerySet of the Item objects associated with this project that do not have a parent Item.

        By default the results will be ordered as defined in the Item model.
        """
        return self.items.filter(parent=None)

    def get_num_children(self):
        """Returns the number of Item objects associated with this project that do not have a parent Item."""
        return self.items.filter(parent=None).count()

    def clean(self):
        """Validates the project's data before saving. Raises ValidationError if invalid data or logic is found.

        - Strip whitespace from the name field
        - Prevent the name field being empty
        """
        super().clean()

        self.name = self.name.strip()  # Strip whitespace

        if not self.name:
            raise ValidationError("Name cannot be empty")

    def save(self, *args, **kwargs):
        """Calls the `clean` method before saving the project."""
        self.clean()
        super().save(*args, **kwargs)


class ProjectOptions(models.Model):
    """An abstract model containing the shared features of the project option models.

    Fields:
        name (str): The name of the setting. Required.
        project (Project): The foreign key of the project to which this item belongs. Required.
        order (int): The index/order of the option. Unique values for each option group per project. Required.
        default (bool): Indicates if this is the default option. Only one per option group per project. Required.

    Methods:
        __str__():
            Returns a string representation of the object in the format: "{project_name}: {option_name}".
        clean():
            Validates the options's data before saving. Raises ValidationError if invalid data or logic is found.
    """

    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE) # related name is set in the child classes
    order = models.PositiveSmallIntegerField()
    default = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __str__(self):
        """Returns a string representation of the object in the format: "{project_name}: {option_name}"."""
        return f"{self.project.name}: {self.name}"

    def clean(self):
        """Validates the options's data before saving. Raises ValidationError if invalid data or logic is found.

        - Enforce unique names for options within the same project.
        - Enforce unique order values for options within the same project.
        - Enforce that only one option within the same project can be the default.
        """
        super().clean()

        if self.__class__.objects.filter(project=self.project, name=self.name).exclude(id=self.id).exists():
            raise ValidationError(_("The option names must be unique within each project."))

        if self.__class__.objects.filter(project=self.project, order=self.order).exclude(id=self.id).exists():
            raise ValidationError(_("The option order values must be unique within each project."))

        if self.default:
            if self.__class__.objects.filter(project=self.project, default=True).exclude(id=self.id).exists():
                raise ValidationError(_("There can only be one default option within each project."))

    def save(self, *args, **kwargs):
        """Calls the `clean` method before saving the item."""
        self.clean()
        super().save(*args, **kwargs)


class ItemTypeOption(ProjectOptions):
    """A model representing the Item Type options, which are set per project.

    Inherits from the ProjectOptions abstract class. Extends with:

    Fields:
        nestable (bool): Indicates if the item type is nestable.
    """
    nestable = models.BooleanField(default=False)

    class Meta:
        default_related_name = 'item_types'


class ItemStatusOption(ProjectOptions):
    """A model representing the Item Status options, which are set per project.

    Inherits from the ProjectOptions abstract class.
    """
    class Meta:
        default_related_name = 'item_statuses'



class ItemPriorityOption(ProjectOptions):
    """A model representing the Item Priority options, which are set per project.

    Inherits from the ProjectOptions abstract class.
    """
    class Meta:
        default_related_name = 'item_priorities'


class Item(AuditMixin, models.Model):
    """A model representing an item within a project in the hierarchical system, which may have hierarchical relationships with other items.

    Inherits from the AuditMixin abstract class.

    Fields:
        name (str): The name of the item. Required.
        changelog (str): A short description of the work done. Not required.
        description (str): A general description of the item. Not required.
        requirements (str): A description of the work that needs to be done. Not required.
        outcome (str): A description of the work that has been done. Not required.
        project (Project): The foreign key of the project to which this item belongs. Required.
        parent (Item): The foreign key to the parent item, creating a hierarchical structure. Not required.
        item_type (ItemTypeOption): The foreign key to the item type. Required.
        item_status (ItemStatusOption): The foreign key to the item status. Required.
        item_priority (ItemPriorityOption): The foreign key to the item priority. Required.
        kanban_row_order (int): The index/order of the item in the kanban column. Unique values within the parent hierarchy. Not required.

    Methods:
        __str__():
            Returns a string representation of the object in the format: "{item_type}: {item_name}".
        get_ancestors():
            Returns a QuerySet of all Item objects that are ancestors of this item in the hierarchy (ie, parent, grandparent, etc). Ordered from root to child.
        get_descendants():
            Returns a QuerySet of all Item objects hierarchically below this item in the hierarchy (ie, children, grandchildren, etc).
        get_children():
            Returns a QuerySet of the Item objects that are directly below this item in the hierarchy (ie, only children).
        get_num_children():
            Returns the number of Item objects that are directly below this item in the hierarchy (ie, only children).
        clean():
            Validates the items's data before saving. Raises ValidationError if invalid data or logic is found.
        save():
            Calls the `clean` method before saving the item.
    """

    name = models.CharField(max_length=100)
    changelog = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    requirements = models.TextField(blank=True)
    outcome = models.TextField(blank=True)
    project = models.ForeignKey(Project, related_name="items", on_delete=models.CASCADE)
    parent = models.ForeignKey("self", blank=True, null=True, related_name="children", on_delete=models.CASCADE)
    item_type = models.ForeignKey(ItemTypeOption, related_name="items", on_delete=models.CASCADE)
    item_status = models.ForeignKey(ItemStatusOption, related_name="items", on_delete=models.CASCADE)
    item_priority = models.ForeignKey(ItemPriorityOption, related_name="items", on_delete=models.CASCADE)
    kanban_row_order = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        ordering = ["item_type", "created_at"]  # order queries by type then oldest first

    def __str__(self):
        """Returns a string representation of the object in the format: "{item_type}: {item_name}"."""
        return f"{self.item_type.name}: {self.name}"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_project = getattr(self, "project", None)

    def get_ancestors(self):
        """Returns a QuerySet of all Item objects that are ancestors of this item in the hierarchy (ie, parent, grandparent, etc).

        By default the results will be ordered from root to child (from top level parent to the item getting it's ancestors).

        Optimised to reduce database queries by traversing the hierarchy in python using the item_ids and parent_ids, then querying for the list of ancestors.
        """
        # Fetch only the necessary fields for the current project
        items = Item.objects.filter(project_id=self.project_id).values_list("id", "parent_id")

        # Build a child->parent relationship lookup dictionary in the format {item_id: parent_id, ...}
        item_lookup = {item[0]: item[1] for item in items}

        ancestor_ids = []
        seen_ancestor_ids = set()
        seen_ancestor_ids.add(self.id)  # first, track the originating id
        current_id = self.parent_id

        # Follow the parent fields upwards for each ancestor until there is no parent
        while current_id:

            # Check for circular references (id already in the ancestors list)
            if current_id in seen_ancestor_ids:
                raise ValidationError(_("An item cannot be its own ancestor."))

            ancestor_ids.append(current_id)
            seen_ancestor_ids.add(current_id)

            # Move to the next ancestor using the lookup dictionary (use item_id to get parent_id)
            current_id = item_lookup.get(current_id)

        # Return the ancestors as a QuerySet, ordered from root to child
        return Item.objects.filter(id__in=reversed(ancestor_ids))

    def get_descendants(self):
        """
        Returns a QuerySet of all Item objects hierarchically below this item in the hierarchy (i.e., children, grandchildren, etc.).

        By default the results will ordered breadth-first, with the siblings (items on the same level), ordered as defined in the Item model.

        Optimised to reduce database queries by traversing the hierarchy in python using the item_ids and child_ids, then querying for the list of descendants.
        """
        # Fetch only the necessary fields (id, parent_id) for all items in the current project
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

        # Return the descendants as a QuerySet, ordered as defined in the Item model
        return Item.objects.filter(id__in=descendants_ids)

    def get_children(self):
        """Returns a QuerySet of the Item objects that are directly below this item in the hierarchy (ie, only children).

        By default the results will be ordered as defined in the Item model.
        """
        return self.children.all()

    def get_num_children(self):
        """Returns the number of Item objects that are directly below this item in the hierarchy (ie, only children)."""
        return self.children.count()

    def clean(self):
        """Validates the items's data before saving. Raises ValidationError if invalid data or logic is found.

        - Strip whitespace from the name field
        - Prevent the name field being empty
        - Prevent an item from changing project once created.
        - Enforce valid item_type choice
        - Enforce valid item_status choice
        - Enforce valid item_priority choice
        - Prevent an item being its own parent
        - Prevent an item having a parent that is in a different project
        - Prevent circular references in the hierarchy
        - Prevent item_types from nesting unless they are nestable types
        - Enforce the ordering of the hierarchy (lower levels cannot be above higher levels)
        """
        super().clean()

        self.name = self.name.strip()  # Strip whitespace

        if not self.name:
            raise ValidationError(_("Name cannot be empty"))

        if self._original_project and self.project != self._original_project:
            raise ValidationError(_("An item cannot change project once created."))

        if self.item_type not in self.project.item_types.all():
            raise ValidationError(_("Invalid item type choice"))

        if self.item_status not in self.project.item_statuses.all():
            raise ValidationError(_("Invalid item status choice"))

        if self.item_priority not in self.project.item_priorities.all():
            raise ValidationError(_("Invalid item priority choice"))

        if self.parent:
            if self == self.parent:
                raise ValidationError(_("An item cannot be its own parent."))

            if self.parent.project != self.project:
                raise ValidationError(_("An item must belong to the same project as its parent."))

            # Prevent circular references in the hierarchy by raising a ValidationError if self is found in the ancestors list
            self.get_ancestors()

            if self.item_type == self.parent.item_type:
                if self.item_type.nestable:
                    pass # Allow nesting of two of the same nestable types
                else:
                    raise ValidationError(_("An item cannot be the same type as its parent unless it is a nestable type."))
            elif self.item_type.order <= self.parent.item_type.order:
                raise ValidationError(
                    _("An item must be 'below' its parent in the hierarchy unless they are of the same nestable type.")
                )

        if self.kanban_row_order:
            if Item.objects.filter(parent=self.parent, kanban_row_order=self.kanban_row_order).exclude(id=self.id).exists():
                raise ValidationError(_("The kanban row order values must be unique within each parent (or null parent)."))


    def save(self, *args, **kwargs):
        """Calls the `clean` method before saving the item."""
        self.clean()
        super().save(*args, **kwargs)
