from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_project, name='create_project'),
    path('<int:pk>/', views.project_detail, name='project_detail'),
    path('add_members/<int:pk>/', views.add_members, name='add_members'),
    path('<int:project_id>/tasks/', views.task_list, name='task_list'),
    path('<int:project_id>/create_task/', views.create_task, name='create_task'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
    path('task/<int:task_id>/update/', views.update_task, name='update_task'),
    path('task/<int:task_id>/complete/', views.complete_task, name='complete_task'),
]
