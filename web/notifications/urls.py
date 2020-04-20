from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='notification-list'),
    path('add/', views.NotificationCreate.as_view(), name='notification-create'),
    path('<int:pk>/edit', views.NotificationEdit.as_view(), name='notification-edit'),
    path('<int:pk>/delete', views.NotificationDelete.as_view(), name='notification-delete'),
]
