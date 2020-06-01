from rest_framework import serializers
from .models import *


class HeroSerializer(serializers.HyperlinkedModelSerializer):
    types = serializers.PrimaryKeyRelatedField(read_only=False, queryset=FoodType.objects.all())
    class Meta:
        model = Food
        fields = ['id', 'name','types']
        #read_only_fields = ('name', 'recipe')