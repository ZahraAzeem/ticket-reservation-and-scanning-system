from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from api.models import Event
from api.serializers import EventSerializer
# Create your views here.

class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
