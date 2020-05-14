"""
http://www.django-rest-framework.org/api-guide/serializers/

"""

from collections import OrderedDict

from rest_framework import serializers


class WritableNestedRelatedField(serializers.SlugRelatedField):

    def __init__(self, model=None, serializer=None, **kwargs):
        assert model is not None, 'The `model` argument is required.'
        assert serializer is not None, 'The `serializer` argument is required.'
        self.model = model
        self.serializer = serializer
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        # TODO maybe also support dict input where we read dict[self.slug_field]
        if not isinstance(data, str):
            self.fail('invalid')
        return super().to_internal_value(data)

    def to_basic_representation(self, obj):
        return super().to_representation(obj)

    def to_representation(self, obj):
        nested = self.serializer(obj, context=self.context)
        return nested.to_representation(obj)

    def get_choices(self, cutoff=None):
        queryset = self.get_queryset()
        if queryset is None:
            # Ensure that field.choices returns something sensible
            # even when accessed with a read-only field.
            return {}

        if cutoff is not None:
            queryset = queryset[:cutoff]

        return OrderedDict([
            (
                self.to_basic_representation(item),
                self.display_value(item)
            )
            for item in queryset
        ])

    def get_queryset(self):
        return self.model.objects.all()
