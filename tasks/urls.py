# tasks/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.TaskListView.as_view(), name='task_list'),
    path('new/', views.TaskCreateView.as_view(), name='task_create'),
    path('<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('<int:pk>/edit/', views.TaskUpdateView.as_view(), name='task_update'),
    path('<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    path('reordenar/', views.TaskReorderView.as_view(), name='task_reorder'),
    path('contato/', views.ContactPageView.as_view(), name='contact_page'),
    path('messages/', views.MessagePageView.as_view(), name='messages'),
]