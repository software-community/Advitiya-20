from rest_framework import serializers

from main_page.models import Events, Talk
from custom_admin.models import Notification

class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Events
        fields = '__all__'

class TalkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Talk
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = '__all__'