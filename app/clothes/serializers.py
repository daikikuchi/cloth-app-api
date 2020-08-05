from rest_framework import serializers

from core.models import Tag, Material


class TagSerializer(serializers.ModelSerializer):
    """Serializer for the tag objects"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class MaterialSerializer(serializers.ModelSerializer):
    """Serializer for material object"""

    class Meta:
        model = Material
        fields = ('id', 'name')
        read_only_fields = ('id',)
