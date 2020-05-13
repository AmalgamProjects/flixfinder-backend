"""

"""

import datetime
from django.db import models


class DateTimeFieldWithoutMicroseconds(models.DateTimeField):
    def to_python(self, value):
        value = super().to_python(value)
        if isinstance(value, datetime.datetime):
            return value.replace(microsecond=0)
        return value

    def get_default(self):
        value = super().get_default()
        if isinstance(value, datetime.datetime):
            return value.replace(microsecond=0)
        return value

    def value_from_object(self, obj):
        value = super().value_from_object(obj)
        if isinstance(value, datetime.datetime):
            return value.replace(microsecond=0)
        return value


class SeparatedValuesField(models.TextField):

    def __init__(self, *args, **kwargs):
        self.token = kwargs.pop('token', ',')
        super(SeparatedValuesField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value: return
        if isinstance(value, list):
            return value
        return value.split(self.token)

    def get_db_prep_value(self, value, connection, prepared=False):
        if not value: return
        assert (isinstance(value, list) or isinstance(value, tuple))
        return self.token.join([unicode(s) for s in value])

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

    def from_db_value(self, value, expression, connection, context):
        value = self.to_python(value)
        return value if value is not None else ''
