# Test Django Backend

## Models

The `organiser` app sets up hierarchical `project`>`item` system where,
- A project contains items.
- An item can nest under another item if it is lower in the hierarchy (eg, Area>Task but not Task>Area).
    - Unless they are of the same time and that type is "nestable" (eg, Task>(sub)Task).
- An item must be in the same project as it's parent.
- An item cannot be it's own ancestor (ie, not A>B>C>A).

Therefore both projects and items can list their:
- Direct `descendants`: items that nest directly under the target.
- All `children`: items that are below the target in the hierarchy (ie, children, grandchildren, etc).

Items can also list their `ancestors`, all items above them in the hierarchy.

Projects hold project-wide settings such as the names, order and nestable state of the item types (eg, Area>Feature>Task, of which only Task is nestable), and the item status options (eg, To Do, In Progress, Done).

Checks in `Model.clean()` have been implemented and tested to enforce a stable hierarchy.

Relationship traversals (eg, climbing up or down to list ancestors or children) are lightly optimised.

## GraphQL

GraphQL provides a nice way to interact with a nestable and listable hierarchy like this, for example to list all the children of a project

    query GetProject($id: ID!) {
        project(id: $id) {
            id
            name
            description
            children {
                id
                name
            }
        }
    }