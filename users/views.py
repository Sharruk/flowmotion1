import json
import logging

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import UserProfile
from .firebase_auth import verify_firebase_token

logger = logging.getLogger(__name__)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'users/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


@csrf_exempt
@require_POST
def google_login_view(request):
    """
    Receives a Firebase ID token from the frontend Google sign-in flow,
    verifies it, and creates or retrieves the corresponding Django user.
    """
    try:
        body = json.loads(request.body)
        id_token = body.get('id_token')
        if not id_token:
            return JsonResponse({'error': 'No ID token provided'}, status=400)

        # Verify the token with Firebase Admin SDK
        decoded_token = verify_firebase_token(id_token)

        email = decoded_token.get('email', '')
        name = decoded_token.get('name', '')
        uid = decoded_token.get('uid', '')

        if not email:
            return JsonResponse({'error': 'No email found in Google account'}, status=400)

        # Get or create the Django user
        user, created = User.objects.get_or_create(
            username=email,
            defaults={
                'email': email,
                'first_name': name.split(' ')[0] if name else '',
                'last_name': ' '.join(name.split(' ')[1:]) if name and len(name.split(' ')) > 1 else '',
            }
        )

        # Make sure a UserProfile exists
        UserProfile.objects.get_or_create(user=user)

        # Set an unusable password for Google-only users (only on first creation)
        if created:
            user.set_unusable_password()
            user.save()

        # Log the user in
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        return JsonResponse({'success': True, 'redirect': '/dashboard/'})

    except Exception as e:
        logger.exception('Google login failed')
        return JsonResponse({'error': f'Authentication failed: {str(e)}'}, status=400)
