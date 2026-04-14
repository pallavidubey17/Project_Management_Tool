from rest_framework import generics, permissions
from .models import Task
from .serializers import TaskSerializer

class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        return Task.objects.filter(project__id=project_id, project__owner=self.request.user)

    def perform_create(self, serializer):
        project_id = self.kwargs['project_id']
        serializer.save(project_id=project_id)

class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        return Task.objects.filter(project__id=project_id, project__owner=self.request.user)