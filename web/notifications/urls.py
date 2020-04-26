from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='notification-list'),
    path('add/', views.NotificationCreate.as_view(), name='notification-create'),
    path('<int:pk>/edit', views.NotificationEdit.as_view(), name='notification-edit'),
    path('<int:pk>/delete', views.NotificationDelete.as_view(), name='notification-delete'),
    path('change_status/<int:pk>', views.ChangeParticipantStatusView.as_view(), name='change-participant-status'),
]
