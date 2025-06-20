# Therefore Knowledge Organisers

A project management system where the items/tasks/todos are used to build knowledge documents. For me to explore Django, GraphQL and Next.js.

## Backend

A Django backend where `Project`s contain `Item`s which can nest under other items to form structures like:

```
Project
    Item (Feature)
        Item (Task)
        Item (Task)
            Item (SubTask)
                Item (SubSubTask)
    Item (Feature)
```

The `ItemType` attribute controls the structure, enforcing an `order` (eg, to prevent features nesting under tasks) and with a self `nestable` flag (eg, to allow tasks to nest under other tasks).

Both projects and items have getters for `descendants` (all items nested under them in the hierarchy) and `children` (only the items nested directly under them).

## GraphQL API

To efficiently work with nested data and related attributes like `ItemType` the backend exposes a graphQL endpoint. For example:

```
{
  projects { # list all projects
    name
    children { # list all direct children of each project
      title
      itemType {
        name
      }
      itemStatus {
        name
      }
      itemLocation {
        name
      }
      numChildren # the number of direct children that each item has
    }
  }
}
```

## Frontend

A Next.js frontend based on an evolving design in Figma.