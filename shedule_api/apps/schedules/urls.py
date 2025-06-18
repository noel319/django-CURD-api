from django.urls import path
from .views import (
    ScheduleListCreateAPIView,
    ScheduleRetrieveUpdateDestroyAPIView,
    protected_endpoint,
    schedule_statistics,
)

app_name = 'schedules'

urlpatterns = [
    path('', ScheduleListCreateAPIView.as_view(), name='schedule-list-create'),
    path('<uuid:id>/', ScheduleRetrieveUpdateDestroyAPIView.as_view(), name='schedule-detail'),
    path('protected/', protected_endpoint, name='protected-endpoint'),
    path('statistics/', schedule_statistics, name='schedule-statistics'),
]