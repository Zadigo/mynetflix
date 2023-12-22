from rest_framework import fields


class CommaSeparatedField(fields.Field):
    """A custom comma separated field for parsing
    and returning comma separated strings"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        if data == '' and self.allow_null:
            return None

        if isinstance(data, list):
            return ', '.join(data)
        return data

    def to_representation(self, value):
        if value is None or value == '':
            return value
        return [value.strip() for value in value.split(',')]
