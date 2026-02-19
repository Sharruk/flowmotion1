from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('habits/', views.habit_list, name='habit_list'),
    path('habits/create/', views.habit_create, name='habit_create'),
    path('habits/<uuid:habit_id>/', views.habit_detail, name='habit_detail'),
    path('habits/<uuid:habit_id>/create_widget/', views.create_widget, name='create_widget'),
    path('habits/<uuid:habit_id>/respond/', views.habit_respond, name='habit_respond'),
    path('habits/<uuid:habit_id>/acknowledge/', views.acknowledge_habit, name='acknowledge_habit'),
    path('history/', views.history, name='history'),
    path('settings/', views.settings_view, name='settings'),
    path('widget/', views.widget_dashboard, name='widget_dashboard'),
    path('habits/<uuid:habit_id>/snooze/', views.snooze_habit, name='snooze_habit'),
]
