from rest_framework import serializers

from core.models import Tag, Material, Shop


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class MaterialSerializer(serializers.ModelSerializer):
    """Serializer for material objects"""

    class Meta:
        model = Material
        fields = ('id', 'name')
        read_only_fields = ('id',)


class ShopSerializer(serializers.ModelSerializer):
    """Serializer for shop objects"""

    class Meta:
        model = Shop
        fields = ('id', 'name', 'link')
        read_only_fields = ('id',)
