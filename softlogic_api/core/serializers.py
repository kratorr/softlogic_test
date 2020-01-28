from core.models import Person
from rest_framework import serializers


class PersonSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Person
        fields = ['id', 'first_name', 'last_name', 'vector']

    def to_representation(self, instance):
        if isinstance(instance, Person):
            return {
                    'id': instance.id,
                    'firt_name': instance.first_name,
                    'last_name': instance.last_name,
                    'has_vector': True if instance.vector else False
            }
        raise Exception('Unexpected type of tagged object')


class PersonUUIDSeriazlier(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id']