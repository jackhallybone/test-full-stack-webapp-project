class BaseCRUD:

    def __init__(self, model):
        self.model = model

    def _parse_input_for_related_fields(self, input):
        input = input or {}
        parsed = {}
        for attr, value in input.items():
            field = self.model._meta.get_field(attr)
            if field.is_relation and isinstance(value, (int, str)):
                related_model = field.related_model
                parsed[attr] = related_model.objects.get(pk=value)
            else:
                parsed[attr] = value
        return parsed

    def create(self, input):
        """Create and object and return it."""
        input = self._parse_input_for_related_fields(input)
        return self.model.objects.create(**input)

    def read_one(self, id):
        """Return one object by its id."""
        return self.model.objects.get(id=id)

    def read_all(self):
        """Return all objects."""
        return self.model.objects.all()

    def update(self, id, input):
        """Update the fields of an object by its id and return it, including object relations."""
        input = self._parse_input_for_related_fields(input)
        instance = self.model.objects.get(pk=id)
        for attr, value in input.items():
            setattr(instance, attr, value)
        instance.full_clean()
        instance.save(update_fields=input.keys())
        return instance

    def delete(self, id):
        """Delete an object by its id and return it."""
        instance = self.model.objects.get(pk=id)
        instance.delete()
        return instance
