# Webapp Test Project

A task management/kanban project to test Django, GraphQL and Next.js.

The idea is to make a nestable task system where the project management views can occur at any level. For example in a

    Project > Area > Feature > Task > Subtask

hierarchy, the it would be possible to view a kanban of all the items under the Project, or only the items under the Feature. That way, you could project manage with different granularity depending on your needs or audience.

## Docker

docker-compose links Django to a PostgreSQL database volume and keeps the node modules off the host machine.

## Next.js

App router layout. Currently running in Docker without turbopack to support hot reloading.