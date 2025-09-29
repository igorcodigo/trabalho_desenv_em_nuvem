from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import ToDoItem
from .serializers import ToDoItemSerializer

# Create your views here.

class ToDoItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to view or edit their to-do items.
    """
    serializer_class = ToDoItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the to-do items
        for the currently authenticated user.
        """
        return ToDoItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
