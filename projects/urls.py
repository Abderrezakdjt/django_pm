from django.urls import path, include
from . import views
from django.views.i18n import set_language


urlpatterns = [
    path('i18n/set_language/', set_language, name='set_language'),
    path('', views.ProjectListView.as_view(), name='Project_list'),
    path('project/create', views.ProjectCreateView.as_view(), name='Project_create'),
    path('project/edit/<int:pk>', views.ProjectUpdateView.as_view(), name='Project_update'),
    path('project/delete/<int:pk>', views.ProjectDeleteView.as_view(), name='Project_delete'),
    path('task/create', views.TaskCreateView.as_view(), name='Task_create'),
    path('task/edit/<int:pk>', views.TaskUpdateView.as_view(), name='Task_update'),
    path('task/delete/<int:pk>', views.TaskDeleteView.as_view(), name='Task_delete'),

]


