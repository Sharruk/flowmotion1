from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from datetime import date, timedelta
from .models import Habit, YesNoHabit, MeasurableHabit, HabitResponse, StreakData
from .ai_utils import get_habit_suggestions, get_emotional_feedback
from .notification_service import send_notification
from .widget_utils import create_habit_widget_shortcut, check_widget_exists

@login_required
def dashboard(request):
    habits = Habit.objects.filter(user=request.user, status='active')
    today = date.today()
    
    habits_data = []
    for habit in habits:
        response = HabitResponse.objects.filter(habit=habit, date=today).first()
        streak, _ = StreakData.objects.get_or_create(habit=habit)
        
        habits_data.append({
            'habit': habit,
            'response': response,
            'streak': streak,
            'completed_today': response.completed if response else False,
        })
    
    context = {
        'habits_data': habits_data,
        'today': today,
    }
    return render(request, 'habits/dashboard.html', context)

@login_required
def habit_list(request):
    habits = Habit.objects.filter(user=request.user)
    return render(request, 'habits/habit_list.html', {'habits': habits})

@login_required
def habit_create(request):
    if request.method == 'POST':
        habit_type = request.POST.get('habit_type', 'yesno')
        name = request.POST.get('name')
        question = request.POST.get('question')
        frequency = request.POST.get('frequency', 'daily')
        notes = request.POST.get('notes', '')
        color = request.POST.get('color', '#6366f1')
        reminder_enabled = request.POST.get('reminder_enabled') == 'on'
        reminder_time = request.POST.get('reminder_time') or None
        
        try:
            ai_data = get_habit_suggestions(name, question or notes)
        except Exception:
            ai_data = None
        
        if habit_type == 'measurable':
            habit = MeasurableHabit.objects.create(
                user=request.user,
                name=name,
                question=question,
                frequency=frequency,
                notes=notes,
                color=color,
                reminder_enabled=reminder_enabled,
                reminder_time=reminder_time,
                unit=request.POST.get('unit', ''),
                target_value=request.POST.get('target_value', 0),
                target_type=request.POST.get('target_type', 'at_least'),
                ai_category=ai_data.get('category') if ai_data else None,
                ai_suggestions=ai_data.get('suggested_tools') if ai_data else None,
                ai_estimated_time=ai_data.get('estimated_time') if ai_data else None,
            )
        else:
            habit = YesNoHabit.objects.create(
                user=request.user,
                name=name,
                question=question,
                frequency=frequency,
                notes=notes,
                color=color,
                reminder_enabled=reminder_enabled,
                reminder_time=reminder_time,
                ai_category=ai_data.get('category') if ai_data else None,
                ai_suggestions=ai_data.get('suggested_tools') if ai_data else None,
                ai_estimated_time=ai_data.get('estimated_time') if ai_data else None,
            )
        
        StreakData.objects.create(habit=habit)
        messages.success(request, f'Habit "{name}" created successfully!')
        return redirect('habit_detail', habit_id=habit.id)
    
    return render(request, 'habits/habit_create.html')

@login_required
def habit_detail(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    today = date.today()
    is_widget_mode = request.GET.get('widget') == 'true'
    widget_exists = check_widget_exists(habit)

    responses = HabitResponse.objects.filter(habit=habit).order_by('-date')[:30]
    streak, _ = StreakData.objects.get_or_create(habit=habit)
    today_response = HabitResponse.objects.filter(habit=habit, date=today).first()
    
    is_measurable = hasattr(habit, 'measurablehabit')
    measurable_data = habit.measurablehabit if is_measurable else None
    
    total_responses = HabitResponse.objects.filter(habit=habit).count()
    completed_responses = HabitResponse.objects.filter(habit=habit, completed=True).count()
    completion_rate = (completed_responses / total_responses * 100) if total_responses > 0 else 0
    
    context = {
        'habit': habit,
        'responses': responses,
        'streak': streak,
        'today_response': today_response,
        'is_measurable': is_measurable,
        'measurable_data': measurable_data,
        'completion_rate': round(completion_rate, 1),
        'is_widget_mode': is_widget_mode,
        'widget_exists': widget_exists,
    }
    
    if is_widget_mode:
        return render(request, 'habits/habit_widget_mode.html', context)
    return render(request, 'habits/habit_detail.html', context)

@login_required
def create_widget(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    success, result = create_habit_widget_shortcut(habit, request)
    if success:
        habit.widget_enabled = True
        habit.save()
        messages.success(request, f"📌 Widget created for this habit!")
    else:
        messages.error(request, f"Could not create widget: {result}")
    return redirect('habit_detail', habit_id=habit.id)

@login_required
def habit_respond(request, habit_id):
    if request.method == 'POST':
        try:
            habit = get_object_or_404(Habit, id=habit_id, user=request.user)
            today = date.today()
            response, created = HabitResponse.objects.get_or_create(
                habit=habit, date=today, defaults={'completed': False}
            )
            
            if hasattr(habit, 'measurablehabit'):
                value = request.POST.get('value', 0)
                try:
                    response.value = float(value) if value else 0
                except (ValueError, TypeError):
                    response.value = 0
                    
                measurable = habit.measurablehabit
                if measurable.target_type == 'at_least':
                    response.completed = response.value >= measurable.target_value
                elif measurable.target_type == 'exactly':
                    response.completed = response.value == measurable.target_value
                else:
                    response.completed = response.value <= measurable.target_value
            else:
                response.completed = request.POST.get('completed') == 'yes'
            
            streak, _ = StreakData.objects.get_or_create(habit=habit)
            if response.completed:
                if streak.last_completed == today - timedelta(days=1):
                    streak.current_streak += 1
                elif streak.last_completed != today:
                    streak.current_streak = 1
                streak.last_completed = today
                if streak.current_streak > streak.best_streak:
                    streak.best_streak = streak.current_streak
            else:
                streak.current_streak = 0
            streak.save()

            # Generate genuine emotional feedback via AI
            try:
                feedback = get_emotional_feedback(habit.name, response.completed, streak.current_streak)
            except Exception:
                feedback = "Great job!" if response.completed else "Keep going!"
                
            response.feedback_message = feedback
            
            if response.completed:
                response.emotional_state = 'happy'
                # Send Linux desktop notification
                try:
                    send_notification("FlowMotion Reminder", feedback)
                except Exception:
                    pass
                messages.success(request, feedback)
            else:
                response.emotional_state = 'neutral'
                messages.info(request, feedback)
            
            response.save()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.accepts('application/json'):
                return JsonResponse({
                    'success': True, 
                    'completed': response.completed, 
                    'emotional_state': response.emotional_state, 
                    'current_streak': streak.current_streak,
                    'feedback': feedback
                })
            return redirect('habit_detail', habit_id=habit.id)
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error in habit_respond: {str(e)}")
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': str(e)}, status=500)
            messages.error(request, "An error occurred while saving your response.")
            return redirect('dashboard')
    return redirect('dashboard')

@login_required
def history(request):
    habits = Habit.objects.filter(user=request.user)
    end_date = date.today()
    start_date = end_date - timedelta(days=30)
    responses = HabitResponse.objects.filter(habit__user=request.user, date__range=[start_date, end_date]).select_related('habit')
    dates = []
    current = start_date
    while current <= end_date:
        dates.append(current)
        current += timedelta(days=1)
    history_data = {}
    for habit in habits:
        history_data[habit.id] = {'habit': habit, 'dates': {d: None for d in dates}}
    for response in responses:
        if response.habit.id in history_data:
            history_data[response.habit.id]['dates'][response.date] = response
    return render(request, 'habits/history.html', {'history_data': history_data, 'dates': dates})

@login_required
def settings_view(request):
    return render(request, 'habits/settings.html')

@login_required
def widget_dashboard(request):
    now = timezone.now()
    next_habit = Habit.objects.filter(user=request.user, status='active', reminder_enabled=True, reminder_time__gte=now.time()).order_by('reminder_time').first()
    if not next_habit:
        next_habit = Habit.objects.filter(user=request.user, status='active', reminder_enabled=True).order_by('reminder_time').first()
    last_response = HabitResponse.objects.filter(habit__user=request.user).order_by('-date', '-created_at').first()
    context = {
        'next_habit': next_habit,
        'emotional_status': last_response.emotional_state if last_response else 'neutral',
        'feedback_message': last_response.feedback_message if last_response else "Start your journey today! 😄",
    }
    return render(request, 'habits/widget.html', context)

@login_required
def snooze_habit(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    messages.info(request, f'Habit "{habit.name}" snoozed for 15 minutes 😐')
    return redirect('widget_dashboard')
