# FlowMotion - Running the Project Locally

## Prerequisites
- Python 3.11 or later
- Linux Environment (for desktop notifications via `notify-send`)
- SQLite3

## Step 1: Clone the Repository
Open your terminal and run:
```bash
git clone <repository-url>
cd flowmotion
```

## Step 2: Install Dependencies
It is recommended to use a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Step 3: Database Setup
Apply migrations to set up your local SQLite database:
```bash
python manage.py migrate
```

## Step 4: Create a Superuser (Optional)
To access the Django admin panel:
```bash
python manage.py createsuperuser
```

## Step 5: Run the Development Server
```bash
python manage.py runserver 0.0.0.0:5000
```
The application will be accessible at `http://localhost:5000`.

## Important Note on Notifications
FlowMotion uses the `notify-send` command for Linux desktop notifications. If you are not on a Linux system or do not have `libnotify` installed, the notifications will log an error in the console but the application will continue to function.
