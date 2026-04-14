from django.urls import path
from .views import TaskListCreateView, TaskRetrieveUpdateDestroyView

urlpatterns = [
    path('<int:project_id>/', TaskListCreateView.as_view(), name='task-list-create'),
    path('<int:project_id>/<int:pk>/', TaskRetrieveUpdateDestroyView.as_view(), name='task-detail'),
]