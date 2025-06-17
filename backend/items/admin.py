from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Item, Project, ItemType, ItemStatus, ItemLocation


class ItemTypeInline(admin.TabularInline):
    model = ItemType
    extra = 1
    fields = ['name', "default", 'order', 'nestable']
    ordering = ['order']


class ItemStatusInline(admin.TabularInline):
    model = ItemStatus
    extra = 1
    fields = ['name', 'default', 'order']
    ordering = ['order']


class ItemLocationInline(admin.TabularInline):
    model = ItemLocation
    extra = 1
    fields = ['name', 'default', 'order']
    ordering = ['order']


class ProjectAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("name", "id", "descendants_count", "updated_at")
    ordering = ["-updated_at"]
    readonly_fields = (
        "created_at",
        # "created_by",
        "updated_at",
        # "updated_by"
    )
    fieldsets = (
        (
            "Description",
            {
                "fields": (
                    "name",
                ),
            },
        ),
        (
            "Audit",
            {
                "fields": (
                    "created_at",
                    # "created_by",
                    "updated_at",
                    # "updated_by",
                ),
            },
        ),
    )
    inlines = [ItemTypeInline, ItemStatusInline, ItemLocationInline]

    def descendants_count(self, obj):
        """Return an html a tag linking to an Item page filter view for all items belonging to a project."""
        item_list_url = reverse("admin:items_item_changelist")
        filtered_item_list_url = f"{item_list_url}?project__id={obj.id}"
        num_descendants = obj.get_num_descendants()
        return format_html('<a href="{}">{}</a>', filtered_item_list_url, num_descendants)


class ItemAdmin(admin.ModelAdmin):
    search_fields = ("title",)
    list_display = ("title", "id", "get_item_type_name", "ancestors_breadcrumb", "updated_at")
    ordering = ["-updated_at"]
    readonly_fields = (
        "created_at",
        # "created_by",
        "updated_at",
        # "updated_by"
    )
    fieldsets = (
        (
            "Settings",
            {
                "fields": (
                    "item_type",
                    "item_status",
                    "item_location",
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
            "Details",
            {
                "fields": (
                    "title",
                    "changelog",
                    "requirements",
                    "outcome",
                ),
            },
        ),
        (
            "Audit",
            {
                "fields": (
                    "created_at",
                    # "created_by",
                    "updated_at",
                    # "updated_by",
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

    def get_item_location_name(self, obj):
        return obj.item_location.name if obj.item_location else None
    get_item_location_name.short_description = 'Item Location'

    def ancestors_breadcrumb(self, obj):
        """Create an html breadcrumb of an item's ancestors with links to each ancestor."""
        ancestors = obj.get_ancestors()
        ancestor_links = [
            format_html(
                '<a href="{}">{}</a>',
                reverse("admin:items_project_change", args=[obj.project.id]),
                str(obj.project),
            )
        ]
        for ancestor in ancestors:
            ancestor_links.append(
                format_html(
                    '<a href="{}">{}</a>', reverse("admin:items_item_change", args=[ancestor.id]), str(ancestor)
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
