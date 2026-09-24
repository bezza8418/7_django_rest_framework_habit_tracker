from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import HabitViewSet, PublicHabitListView

router = DefaultRouter()
router.register(r'habits', HabitViewSet, basename='habit')
router.register(r'public-habits', PublicHabitListView, basename='public-habit')

urlpatterns = router.urls
