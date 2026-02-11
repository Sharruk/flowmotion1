# FlowMotion - Intelligent Habit Tracking

## Overview
FlowMotion is a full-stack Django web application for habit and task management. It provides habit tracking with streaks, completion history, and visualization through Chart.js.

## Tech Stack
- **Backend**: Python 3.11, Django 5.x
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Charts**: Chart.js
- **APIs**: Django REST Framework

## Project Structure
```
flowmotion/          # Django project settings
habits/              # Habit management app (models, views, APIs)
users/               # User authentication app
analytics/           # Analytics app (placeholder)
templates/           # HTML templates
static/              # CSS and JavaScript files
```

## Running the Application
The app runs on port 5000 using Django's development server:
```
python manage.py runserver 0.0.0.0:5000
```

## Features
- User registration and authentication
- Yes/No habits (binary completion)
- Measurable habits (quantitative tracking)
- Streak tracking
- History calendar view
- Chart.js visualizations
- REST API endpoints

## API Endpoints
- `/api/habits/` - List all habits
- `/api/habits/<id>/` - Habit details
- `/api/habits/<id>/responses/` - Habit responses
- `/api/stats/` - User statistics

## Key URLs
- `/` - Dashboard (requires login)
- `/login/` - Login page
- `/register/` - Registration page
- `/habits/` - Habit list
- `/habits/create/` - Create new habit
- `/history/` - History view
- `/settings/` - User settings

## Background Processes
Notifications are executed using a background APScheduler process invoking Linux’s notify-send utility. Due to cloud environment limitations, desktop alerts are demonstrated on local Ubuntu systems.
