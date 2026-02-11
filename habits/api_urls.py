from django.urls import path
from . import api_views
from . import notifications_api

urlpatterns = [
    path('habits/', api_views.habit_list_api, name='api_habit_list'),
    path('habits/<uuid:habit_id>/', api_views.habit_detail_api, name='api_habit_detail'),
    path('habits/<uuid:habit_id>/responses/', api_views.habit_responses_api, name='api_habit_responses'),
    path('stats/', api_views.stats_api, name='api_stats'),
    path('reminders/', notifications_api.habit_reminders_api, name='api_reminders'),
]

