from rest_framework import serializers

from main_page.models import Events, Talk, Coordinator
from custom_admin.models import Notification


class EventSerializer(serializers.ModelSerializer):
    coordinator = serializers.SerializerMethodField()

    class Meta:
        model = Events
        fields = '__all__'

    def get_coordinator(self, instance):
        return {'name': instance.coordinator.name, 'mobile': instance.coordinator.phone}


class TalkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Talk
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = '__all__'
