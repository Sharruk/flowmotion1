# FlowMotion - Intelligent Habit Tracking

## Overview
FlowMotion is a full-stack Django web application for habit and task management. It provides AI-powered habit tracking with streaks, completion history, advanced statistics, and visualization through Chart.js.

## Tech Stack
- **Backend**: Python 3.11, Django 5.x
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Charts**: Chart.js
- **APIs**: Django REST Framework
- **AI Integration**: Google Gemini API, Groq API
- **Authentication**: Firebase + Django Sessions
- **Desktop Widgets**: Linux .desktop shortcuts with dynamic emoji icons

## Project Structure
```
flowmotion/          # Django project settings
habits/              # Habit management (models, views, APIs, statistics)
users/               # Authentication (Firebase + Django)
templates/           # HTML templates
static/              # CSS, JS, emoji icons
```

## Key Features
- ✅ User registration & authentication (Firebase + Django)
- ✅ Yes/No habits & Measurable habits
- ✅ Smart streaks (current & best)
- ✅ Weekly completion charts
- ✅ Monthly progress visualization
- ✅ AI-powered habit recommendations
- ✅ Emotional feedback system
- ✅ 3-stage reminders (pre, main, post)
- ✅ Desktop widgets with live updates
- ✅ Statistics dashboard
- ✅ REST API endpoints

## Statistics & Analytics
### Dashboard
- Weekly Completion Rate
- Overall Completion Rate
- Active Habits Count
- Weekly Bar Chart (Mon-Sun)

### Habit Detail
- Current Streak
- Best Streak
- Completion Rate %
- Total Completions
- Weekly Bar Chart
- Monthly Line Chart

## API Endpoints
- `GET /api/stats/` - Dashboard statistics
- `GET /api/habits/` - List habits with stats
- `GET /api/habits/<id>/` - Habit details
- `GET /api/habits/<id>/responses/` - Responses with weekly data

## Key URLs
- `/` → Dashboard
- `/login/` → Firebase Sign-In
- `/register/` → Registration
- `/habits/<id>/` → Habit detail
- `/widgets/` → Widget management
- `/history/` → History
- `/settings/` → Settings

## Recent Implementations
- **Statistics Module**: `habits/statistics.py` - Weekly data, streaks, completion rates
- **Chart.js Integration**: Weekly/monthly visualization with real data
- **Google Sign-In**: Proper redirect flow
- **Desktop Widgets**: Dynamic emoji icons (🙂 😐 😟 🔥)
- **Session Management**: Secure Django sessions

## Running
```
python manage.py runserver 0.0.0.0:5000
```
