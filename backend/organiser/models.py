from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from organiser.mixins import AuditMixin


class Project(AuditMixin, models.Model):
    """The model representing a project in the hierarchical system.

    Inherits from the AuditMixin abstract class.

    Fields:
        name (str): The name of the project. Required.

    Methods:
        __str__():
            Returns a string representation of the project with its name in the format "Project: {name}"
        get_default_item_type():
            Get the ItemType object associated with this project that is set to default.
        get_default_item_status():
            Get the ItemStatus object associated with this project that is set to default.
        get_default_item_location():
            Get the ItemLocation object associated with this project that is set to default.
        get_descendants():
            Returns a QuerySet of all Item objects associated with this project.
        get_children():
            Returns a QuerySet of the Item objects associated with this project that do not have a parent Item.
        get_num_children():
            Returns the number of Item objects associated with this project that do not have a parent Item.
        clean():
            Validates the model data before saving. Raises ValidationError if invalid data or logic is found.
        save():
            Calls the `clean` method before saving the project.
    """

    name = models.CharField(max_length=100)

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

    def get_default_item_location(self):
        """Get the ItemLocation object associated with this project that is set to default."""
        return self.item_location.filter(default=True).first()

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
        """Validates the model data before saving. Raises ValidationError if invalid data or logic is found.

        - Strip whitespace from the start and end of the name
        - The name field must not be empty
        """
        super().clean()

        self.name = self.name.strip()  # Strip whitespace

        if not self.name:
            raise ValidationError("Name cannot be empty")

    def save(self, *args, **kwargs):
        """Calls the `clean` method before saving the project."""
        self.clean()
        super().save(*args, **kwargs)


class ItemType(models.Model):
    """A model representing the type of an item in the hierarchical system.

    Fields:
        project (Project): The foreign key of the project to which this item belongs. Required.
        name (str): The name of the type. Required.
        default (bool): Indicates if this is the default type option for items in the project. Required.
        order (int): The logical order of the types in the project. Required.
        nestable (bool): Indicates if an item of this type can be nested within an item of the same type.

    Methods:
        __str__():
            Returns a string representation of the object in the format: "{project name}: {item type name}".
        clean():
            Validates the model data before saving. Raises ValidationError if invalid data or logic is found.
    """

    project = models.ForeignKey(Project, related_name="item_types", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    default = models.BooleanField(default=False)
    order = models.SmallIntegerField()
    nestable = models.BooleanField(default=False)

    class Meta:
        ordering = ["order"]  # order queries by order

    def __str__(self):
        """Returns a string representation of the object in the format: "{project name}: {item type name}"."""
        return f"{self.project.name}: {self.name}"

    @staticmethod
    def default_options():
        """Define a set of default types for when creating a new project."""
        return [
            {'name': _('Area'), 'default': False, 'order': 1, 'nestable': False},
            {'name': _('Epic'), 'default': False, 'order': 2, 'nestable': False},
            {'name': _('Feature'), 'default': False, 'order': 3, 'nestable': False},
            {'name': _('Task'), 'default': True, 'order': 4, 'nestable': True},
        ]

    def clean(self):
        """Validates the model data before saving. Raises ValidationError if invalid data or logic is found.

        - Strip whitespace from the start and end of the name
        - The name field must not be empty
        - Name must be unique within each project
        - There can only be one default option within each project
        - Order must be unique within each project
        """
        super().clean()

        self.name = self.name.strip()  # Strip whitespace

        if not self.name:
            raise ValidationError("Name cannot be empty")

        if ItemType.objects.filter(project=self.project, name=self.name).exclude(id=self.id).exists():
            raise ValidationError(_("Item type names must be unique within each project."))

        if self.default:
            if ItemType.objects.filter(project=self.project, default=True).exclude(id=self.id).exists():
                raise ValidationError(_("There can only be one default item type within each project."))

        if ItemType.objects.filter(project=self.project, order=self.order).exclude(id=self.id).exists():
            raise ValidationError(_("Item type order must be unique within each project."))

    def save(self, *args, **kwargs):
        """Calls the `clean` method before saving the item."""
        self.clean()
        super().save(*args, **kwargs)


class ItemStatus(models.Model):
    """A model representing the status of an item in the hierarchical system.

    Fields:
        project (Project): The foreign key of the project to which this item belongs. Required.
        name (str): The name of the status. Required.
        default (bool): Indicates if this is the default status option for items in the project. Required.
        order (int): The logical order of the statuses in the project. Required.

    Methods:
        __str__():
            Returns a string representation of the object in the format: "{project name}: {item status name}".
        clean():
            Validates the data before saving. Raises ValidationError if invalid data or logic is found.
    """

    project = models.ForeignKey(Project, related_name="item_statuses", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    default = models.BooleanField(default=False)
    order = models.SmallIntegerField()

    class Meta:
        ordering = ["order"]  # order queries by order

    def __str__(self):
        """Returns a string representation of the object in the format: "{project name}: {item status name}"."""
        return f"{self.project.name}: {self.name}"

    @staticmethod
    def default_options():
        """Define a set of default statuses for when creating a new project."""
        return [
            {'name': _('To Do'), 'default': True, 'order': 1},
            {'name': _('In Progress'), 'default': False, 'order': 2},
            {'name': _('Done'), 'default': False, 'order': 3},
        ]

    def clean(self):
        """Validates the model data before saving. Raises ValidationError if invalid data or logic is found.

        - Strip whitespace from the start and end of the name
        - The name field must not be empty
        - Name must be unique within each project
        - There can only be one default option within each project
        """
        super().clean()

        self.name = self.name.strip()  # Strip whitespace

        if not self.name:
            raise ValidationError("Name cannot be empty")

        if ItemStatus.objects.filter(project=self.project, name=self.name).exclude(id=self.id).exists():
            raise ValidationError(_("Item status names must be unique within each project."))

        if self.default:
            if ItemStatus.objects.filter(project=self.project, default=True).exclude(id=self.id).exists():
                raise ValidationError(_("There can only be one default item status within each project."))

    def save(self, *args, **kwargs):
        """Calls the `clean` method before saving the item."""
        self.clean()
        super().save(*args, **kwargs)


class ItemLocation(models.Model):
    """A model representing the location of an item in the hierarchical system.

    Fields:
        project (Project): The foreign key of the project to which this item belongs. Required.
        name (str): The name of the location. Required.
        default (bool): Indicates if this is the default location option for items in the project. Required.
        order (int): The logical order of the locations in the project. Required.

    Methods:
        __str__():
            Returns a string representation of the object in the format: "{project name}: {item location name}".
        clean():
            Validates the data before saving. Raises ValidationError if invalid data or logic is found.
    """

    project = models.ForeignKey(Project, related_name="item_locations", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    default = models.BooleanField(default=False)
    order = models.SmallIntegerField()

    class Meta:
        ordering = ["order"]  # order queries by order

    def __str__(self):
        """Returns a string representation of the object in the format: "{project name}: {item location name}"."""
        return f"{self.project.name}: {self.name}"

    @staticmethod
    def default_options():
        """Define a set of default locations for when creating a new project."""
        return [
            {'name': _('Backlog'), 'default': True, 'order': 1},
            {'name': _('Board'), 'default': False, 'order': 2},
            {'name': _('Cleared'), 'default': False, 'order': 3},
        ]

    def clean(self):
        """Validates the model data before saving. Raises ValidationError if invalid data or logic is found.

        - Strip whitespace from the start and end of the name
        - The name field must not be empty
        - Name must be unique within each project
        - There can only be one default option within each project
        """
        super().clean()

        self.name = self.name.strip()  # Strip whitespace

        if not self.name:
            raise ValidationError("Name cannot be empty")

        if ItemLocation.objects.filter(project=self.project, name=self.name).exclude(id=self.id).exists():
            raise ValidationError(_("Item location names must be unique within each project."))

        if self.default:
            if ItemLocation.objects.filter(project=self.project, default=True).exclude(id=self.id).exists():
                raise ValidationError(_("There can only be one default item location within each project."))

    def save(self, *args, **kwargs):
        """Calls the `clean` method before saving the item."""
        self.clean()
        super().save(*args, **kwargs)


class Item(AuditMixin, models.Model):
    """A model representing an item within a project in the hierarchical system, which may have hierarchical relationships with other items.

    Inherits from the AuditMixin abstract class.

    Fields:
        project (Project): The foreign key of the project to which this item belongs. Required.
        parent (Item): The foreign key to the parent item, creating a hierarchical structure.
        item_type (ItemType): The foreign key to the item type. Required.
        item_status (ItemStatus): The foreign key to the item status. Required.
        item_location (ItemLocation): The foreign key to the item location. Required.
        title (str): A summary of what needs to be done. Required.
        changelog (str): A summary of what has been done.
        requirements (str): A description of what needs to be done.
        outcomes (str): A description of what was done.

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
            Validates the model data before saving. Raises ValidationError if invalid data or logic is found.
        save():
            Calls the `clean` method before saving the item.
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
        """Returns a string representation of the object in the format: "{item_type}: {item_title}"."""
        return f"{self.item_type.name}: {self.title}"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_project = getattr(self, "project", None)

    def get_ancestors(self):
        """Returns a QuerySet of all Item objects that are ancestors of this item in the hierarchy (ie, parent, grandparent, etc).

        By default the results will be ordered from root to child (from top level parent to the item getting it's ancestors).

        Optimised to reduce database queries by traversing the hierarchy in python using the item_ids and parent_ids, then querying for the list of ancestors.
        """
        # Fetch only the necessary fields for traversing the ancestry (id, parent_id) for all items in the current project
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

        # Return the descendants as a QuerySet, ordered as defined in the Item model
        return Item.objects.filter(id__in=descendants_ids)

    # TODO:
    # - find decendants (query for all then search and find a list of IDs of the decendants)
    # - num_decendatns (just the number of IDs in above)
    # - get_decendants (runs a query on the results of the find)


    # def find_descendants(self):
    #     """Searches for all descendants (children, grandchildren, etc) of the item.

    #     Returns a list of their IDs.
    #     """

    #     # Fetch only the necessary fields for traversing the ancestry (id, parent_id) for all items in the current project
    #     items = Item.objects.filter(project_id=self.project_id).values_list("id", "parent_id")

    #     # Build a parent->children relationship lookup dictionary in the format {parent_id: [child_id, ...], ...}
    #     child_lookup = {}
    #     for item_id, parent_id in items:
    #         child_lookup.setdefault(parent_id, []).append(item_id)

    #     descendants_ids = []
    #     parent_ids_to_process = [self.id]

    #     # Traverse the hierarchy starting from this item's ID
    #     while parent_ids_to_process:
    #         parent_id = parent_ids_to_process.pop(0)  # First-in-first-out
    #         children_ids = child_lookup.get(parent_id, [])
    #         descendants_ids.extend(children_ids)
    #         parent_ids_to_process.extend(children_ids)

    #     return descendants_ids

    # def get_num_descendants(self):
    #     descendants_ids = self.find_descendants()
    #     return len(descendants_ids)

    # def get_decendants(self):
    #     descendants_ids = self.find_descendants()
    #     return Item.objects.filter(id__in=descendants_ids)




















    def get_children(self):
        """Returns a QuerySet of the Item objects that are directly below this item in the hierarchy (ie, only children).

        By default the results will be ordered as defined in the Item model.
        """
        return self.children.all()

    def get_num_children(self):
        """Returns the number of Item objects that are directly below this item in the hierarchy (ie, only children)."""
        return self.children.count()

    def clean(self):
        """Validates the model data before saving. Raises ValidationError if invalid data or logic is found.

        - Strip whitespace from the start and end of the title
        - The title field must not be empty
        - The type must be a type within the same project
        - The status must be status within the same project
        - The location must be a location within the same project
        - An item cannot be it's one parent
        - An item must belong to the same project as it's parent
        - Prevent circular referencing in the parent field
        - Prevent an item from nesting under an item of the same type unless that type is nestable
        - Items can only nest under items of a higher (ordered) type, unless the type is nestable
        """
        super().clean()

        self.title = self.title.strip()  # Strip whitespace

        if not self.title:
            raise ValidationError(_("Title cannot be empty"))

        if self._original_project and self.project != self._original_project:
            raise ValidationError(_("An item cannot change project once created."))

        if self.item_type not in self.project.item_types.all():
            raise ValidationError(_("Invalid item type choice"))

        if self.item_status not in self.project.item_statuses.all():
            raise ValidationError(_("Invalid item status choice"))

        if self.item_location not in self.project.item_locations.all():
            raise ValidationError(_("Invalid item location choice"))

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

    def save(self, *args, **kwargs):
        """Calls the `clean` method before saving the item."""
        self.clean()
        super().save(*args, **kwargs)
