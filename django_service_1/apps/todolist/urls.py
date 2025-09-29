from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ToDoItemViewSet

router = DefaultRouter()
router.register(r'', ToDoItemViewSet, basename='todoitem')

urlpatterns = [
    path('', include(router.urls)),
]
