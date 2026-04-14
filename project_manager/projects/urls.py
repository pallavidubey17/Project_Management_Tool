from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('create/', views.create_project, name='create_project'),
    path('<int:pk>/', views.project_detail, name='project_detail'),
]