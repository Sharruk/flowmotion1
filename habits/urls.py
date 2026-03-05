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
    path('widgets/', views.widgets_list, name='widgets_list'),
    path('widgets/create/', views.create_widget_choice, name='create_widget_choice'),
    path('widgets/create/habit/', views.create_habit_widget, name='create_habit_widget'),
    path('widgets/create/countdown/', views.create_countdown_widget, name='create_countdown_widget'),
    path('widgets/create/countdown/<int:widget_id>/shortcut/', views.create_countdown_shortcut, name='create_countdown_shortcut'),
    path('widgets/view/<int:widget_id>/', views.view_countdown_widget, name='view_countdown_widget'),
    path('history/', views.history, name='history'),
    path('settings/', views.settings_view, name='settings'),
    path('widget/', views.widget_dashboard, name='widget_dashboard'),
    path('habits/<uuid:habit_id>/snooze/', views.snooze_habit, name='snooze_habit'),
]
