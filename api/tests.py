# api/tests.py

import uuid

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Event, Ticket


User = get_user_model()


class TicketAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="zahra",
            password="testpass123",
        )

        self.event = Event.objects.create(
            name="Calvin Haris Concert",
            date="2026-12-20T10:00:00Z",
            venue="Valencia, Lahore",
            total_ticket_capacity=1,
            available_ticket_count=1,
        )
        # Ensuring user is authenticated to create tickets because in viewset we are using current user to create tickets
        self.client.force_authenticate(user=self.user)

    def test_user_can_reserve_available_ticket(self):
        # to get /api/tickets/
        url = reverse("ticket-list")

        response = self.client.post(url,
            {"event": self.event.id},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

     #Requirement that the event cannot be overbooked
    def test_event_cannot_be_overbooked(self):
        # First user books a ticket for the event
        first_response = self.client.post(
            reverse("ticket-list"),
            {"event": self.event.id},
            format="json",
        )
        # second user tries to book a ticket for the same event
        second_user = User.objects.create_user(username="second-user",password="testpass123")
        self.client.force_authenticate(user=second_user)

        second_response = self.client.post(
            reverse("ticket-list"),
            {"event": self.event.id},
            format="json",
        )

        self.assertEqual(first_response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(second_response.status_code,status.HTTP_400_BAD_REQUEST)



    def test_ticket_cannot_be_scanned_twice(self):
        ticket = Ticket.objects.create(
            user=self.user,
            event=self.event,
            status="valid",
        )

        url = reverse("ticket-scan")
        payload = {"qr_token": str(ticket.qr_token)}

        first_response = self.client.post(url, payload, format="json")
        second_response = self.client.post(url, payload, format="json")

        self.assertEqual(first_response.status_code,status.HTTP_200_OK)
        self.assertEqual(second_response.status_code,status.HTTP_400_BAD_REQUEST)