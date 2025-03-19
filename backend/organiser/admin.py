from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Item, Project, ItemTypeOption, ItemStatusOption, ItemPriorityOption


class ItemTypeOptionInline(admin.TabularInline):
    model = ItemTypeOption
    extra = 1
    fields = ['name', 'order', 'nestable', 'default']
    ordering = ['order']


class ItemStatusOptionInline(admin.TabularInline):
    model = ItemStatusOption
    extra = 1
    fields = ['name', 'order', 'default']
    ordering = ['order']


class ItemPriorityOptionInline(admin.TabularInline):
    model = ItemPriorityOption
    extra = 1
    fields = ['name', 'order', 'default']
    ordering = ['order']


class ProjectAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("name", "id", "descendants_count", "updated_at")
    ordering = ["-updated_at"]
    readonly_fields = ("created_at", "created_by", "updated_at", "updated_by")
    fieldsets = (
        (
            "Description",
            {
                "fields": (
                    "name",
                    "description",
                ),
            },
        ),
        (
            "Audit",
            {
                "fields": (
                    "created_at",
                    "created_by",
                    "updated_at",
                    "updated_by",
                ),
            },
        ),
    )
    inlines = [ItemTypeOptionInline, ItemStatusOptionInline, ItemPriorityOptionInline]

    def descendants_count(self, obj):
        """Count the number of descendants, and link to an Item view filtered for the project."""
        # Generate a URL to the items page with a filter for the current project
        url = reverse("admin:organiser_item_changelist")
        url_with_filter = f"{url}?project__id={obj.id}"
        return format_html('<a href="{}">{}</a>', url_with_filter, obj.get_descendants().count())


class ItemAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("name", "id", "get_item_type_name", "ancestors_path", "updated_at")
    ordering = ["-updated_at"]
    readonly_fields = ("created_at", "created_by", "updated_at", "updated_by")
    fieldsets = (
        (
            "Description",
            {
                "fields": (
                    "name",
                    "changelog",
                    "description",
                    "requirements",
                    "outcome",
                    "item_type",
                    "item_status",
                    "item_priority",
                ),
            },
        ),
        (
            "Hierarchy",
            {
                "fields": (
                    "project",
                    "parent",
                ),
            },
        ),
        (
            "Organisation",
            {
                "fields": (
                    "kanban_row_order",
                ),
            },
        ),
        (
            "Audit",
            {
                "fields": (
                    "created_at",
                    "created_by",
                    "updated_at",
                    "updated_by",
                ),
            },
        ),
    )

    def get_item_type_name(self, obj):
        return obj.item_type.name if obj.item_type else None
    get_item_type_name.short_description = 'Item Type'

    def get_item_status_name(self, obj):
        return obj.item_status.name if obj.item_status else None
    get_item_status_name.short_description = 'Item Status'

    def get_item_priority_name(self, obj):
        return obj.item_priority.name if obj.item_priority else None
    get_item_priority_name.short_description = 'Item Priority'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'item_type' or db_field.name == 'item_status' or db_field.name == 'item_priority':
            # Return all the items, regardless of the project
            kwargs['queryset'] = db_field.remote_field.model.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def ancestors_path(self, obj):
        """Create a linked ancestors path in the format 'project / parent / parent / ...'."""
        ancestors = obj.get_ancestors()
        ancestor_links = [
            format_html(
                '<a href="{}">{}</a>',
                reverse("admin:organiser_project_change", args=[obj.project.id]),
                str(obj.project),
            )
        ]
        for ancestor in ancestors:
            ancestor_links.append(
                format_html(
                    '<a href="{}">{}</a>', reverse("admin:organiser_item_change", args=[ancestor.id]), str(ancestor)
                )
            )
        return format_html(" / ".join(ancestor_links))

    def get_readonly_fields(self, request, obj=None):
        # Project can be set on creation, but is readonly once set
        if obj:
            return self.readonly_fields + ("project",)
        return self.readonly_fields


admin.site.register(Project, ProjectAdmin)
admin.site.register(Item, ItemAdmin)
