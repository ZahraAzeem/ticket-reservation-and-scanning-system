from rest_framework.routers import DefaultRouter

from api.views import EventViewSet, TicketViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')
router.register(r'tickets', TicketViewSet, basename='ticket')  

urlpatterns = router.urls
