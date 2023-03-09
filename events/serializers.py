from rest_framework import serializers
from .models import Event
from users.serializers import MyUserSerializer

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class PopulatedEventSerializer(EventSerializer):
    host = MyUserSerializer()

