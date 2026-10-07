import uuid

from django.db import models

from django.conf import settings

# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField()
    venue = models.CharField(max_length=100)
    total_ticket_capacity = models.PositiveIntegerField()
    available_ticket_count = models.PositiveIntegerField()  
    
    def __str__(self):
        return '{event} at {venue}'.format(event=self.name, venue=self.venue)
    

STATUS ={
    'AVAILABLE': 'available',
    'VALID': 'valid',
    'CANCELLED': 'cancelled',
    'USED': 'used',
}

class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[(status, status) for status in STATUS.values()], default=STATUS['AVAILABLE'])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # we dont need an integer id for the ticket because we can use the qr_token as a unique identifier for the ticket. This will be used to validate the ticket when the user presents it at the event. The qr_token will be a UUID which is unique and hard to guess.
    qr_token = models.UUIDField(default=uuid.uuid4,unique=True,editable=False)

    def __str__(self):
        return 'Ticket for {event} - Status: {status}'.format(event=self.event.name, status=self.status)