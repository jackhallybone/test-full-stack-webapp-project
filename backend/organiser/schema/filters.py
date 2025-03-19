def filter_projects(queryset, name_contains=None):
    """Filter a QuerySet of Projects by the provided field fields.

    Will return the original QuerySet if no filter arguments provided or an empty QuerySet if no results satisfy the filters.

    Arguments:
        queryset (QuerySet): The input QuerySet of Projects to be filtered.
        name_contains (str): A (sub)string to (icontains) search the name fields for.

    Returns:
        queryset (QuerySet): The filtered QuerySet.
    """
    if name_contains:
        queryset = queryset.filter(name__icontains=name_contains)
    return queryset


def filter_items(queryset, name_contains=None, project=None, item_type=None, item_status=None, item_priority=None):
    """Filter a QuerySet of Items by the provided field fields.

    Will return the original QuerySet if no filter arguments provided or an empty QuerySet if no results satisfy the filters.

    Arguments:
        queryset (QuerySet): The input QuerySet of Items to be filtered.
        name_contains (str): A (sub)string to (icontains) search the name fields for.
        project (ID): A Project ID to filter the project field by.
        item_type (ID): An ItemType ID to filter the item_type field by.
        item_status (ID): An ItemStatus ID to filter the item_status field by.
        item_priority (ID): An ItemPriority ID to filter the item_priority field by.

    Returns:
        queryset (QuerySet): The filtered QuerySet.
    """
    if name_contains:
        queryset = queryset.filter(name__icontains=name_contains)
    if project:
        queryset = queryset.filter(project=project)
    if item_type:
        queryset = queryset.filter(item_type=item_type)
    if item_status:
        queryset = queryset.filter(item_status=item_status)
    if item_priority:
        queryset = queryset.filter(item_priority=item_priority)
    return queryset
