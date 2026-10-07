from rest_framework.decorators import action
from rest_framework import serializers
from rest_framework import mixins, status, viewsets
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from api.models import Event, Ticket
from api.serializers import EventSerializer, TicketSerializer
# Create your views here.

class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    
    def perform_create(self, serializer):
        serializer.save(available_ticket_count=serializer.validated_data["total_ticket_capacity"])
    

class TicketViewSet(mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,):
    
    serializer_class = TicketSerializer
    
    def get_queryset(self):
        # filter out the current users's tickets with the user and event
        # we are using select_related because a ticket is related to only one event and one user + to optimize the query
        return (
            Ticket.objects.filter(user=self.request.user).select_related("event", "user")
        )
    
    def perform_create(self, serializer):
        user_sent_event = serializer.validated_data["event"]
        event = Event.objects.select_for_update().get(
            id=user_sent_event.id
        )
        
        # checking for available tickets
        if event.available_ticket_count <= 0:
            raise serializers.ValidationError({
                "event": "No tickets are available for this event."
            })

        event.available_ticket_count -= 1
        # updating only the required field to avoid race conditions and stale saves like if some other service has changed the event fields in the database and we are saving the whole event object, it will overwrite those changes with stale data. So we are only updating the available_ticket_count field.
        event.save(update_fields=["available_ticket_count"])

        serializer.save(
            user=self.request.user,
            event=event,
            status="valid",
        )
        
    @action(detail=True, methods=['post'])
    def cancel(self, request):
        ticket = self.get_object()
        if ticket.status == 'valid':
            ticket.status = 'cancelled'
            ticket.save()
            event = ticket.event
            event.available_ticket_count += 1
            event.save(update_fields=["available_ticket_count"])
            return Response({'status': 'Ticket cancelled successfully.'})
        else:
            return Response({'status': 'Ticket cannot be cancelled.'}, status=status.HTTP_400_BAD_REQUEST)
        
