from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='tasks'),
    path('<int:id>/', views.task_detail, name='task_detail'),
    path('create/', views.create_task, name='create_task'),
]
