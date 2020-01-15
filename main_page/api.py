from rest_framework import viewsets
from rest_framework.permissions import BasePermission, SAFE_METHODS

from main_page.models import Events, Talk
from custom_admin.models import Notification
from main_page.serializers import EventSerializer, TalkSerializer, NotificationSerializer


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class EventViewSet(viewsets.ModelViewSet):
    queryset = Events.objects.all()
    serializer_class = EventSerializer
    permission_classes = [ReadOnly]

class TalkViewSet(viewsets.ModelViewSet):
    queryset = Talk.objects.all()
    serializer_class = TalkSerializer
    permission_classes = [ReadOnly]

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [ReadOnly]
    