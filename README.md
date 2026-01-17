# FlowMotion - Intelligent Habit and Task Management System

FlowMotion is an intelligent habit and task management system designed for Linux desktop users. It helps you track habits, manage tasks, and provides smart reminders and emotional feedback.

## Features
- **Habit Tracking**: Support for binary (Yes/No) and measurable habits.
- **Smart Scheduling**: Adaptive reminder logic that learns from your behavior.
- **Linux Notifications**: Native desktop notifications using `notify-send`.
- **AI Integration**: AI-powered task understanding and categorization.
- **Visual Analytics**: Beautiful charts using Chart.js to track your progress.
- **Emotional Feedback**: Supportive messages based on your performance.

## Tech Stack
- **Backend**: Python 3.9+, Django 4.x
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **API**: Django REST Framework
- **Charts**: Chart.js

## Installation and Setup (Linux Ubuntu)

### 1. Install System Dependencies
Ensure you have Python 3 and `libnotify-bin` (for notifications) installed:
```bash
sudo apt update
sudo apt install python3 python3-pip libnotify-bin
```

### 2. Clone and Setup Environment
```bash
# Clone the repository (or navigate to the project folder)
cd flowmotion

# Install Python dependencies
pip install -r requirements.txt
```

### 3. Initialize Database
```bash
python manage.py migrate
```

### 4. Run the Application
```bash
python manage.py runserver
```
The application will be available at `http://localhost:8000`.

## Key Components
- `habits/`: Core logic for habit management and tracking.
- `users/`: User profiles and preference management.
- `analytics/`: Data processing for charts and progress tracking.
- `flowmotion/`: Project configuration and settings.

## Note on Notifications
The application uses `notify-send` for desktop notifications. Ensure your Linux environment supports desktop notifications to see these in action.
