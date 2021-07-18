from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.db.models import Model


def get_serializer(entity: Model) -> ModelSerializer:
    """ 
    Create a new serializer class avoiding overwriting the previous one

    Parameters
    ----------
    entity: class

    Returns
    -------
    A new BaseSerializer class
    """
    class BaseSerializer(ModelSerializer):
        class Meta:
            model = entity
            fields = '__all__'

    return BaseSerializer


class OutputPagedViewSerializer(serializers.Serializer):
    offset = serializers.IntegerField()
    limit = serializers.IntegerField()
    total_records = serializers.IntegerField()
    records = serializers.ListField()


class InputPagedViewSerializer(serializers.Serializer):
    offset = serializers.IntegerField(default=0)
    limit = serializers.IntegerField(default=50, min_value=0, max_value=100)
