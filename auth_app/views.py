from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import UserProfile
import json

def login_view(request):
    # If user is already logged in, redirect appropriately
    if request.user.is_authenticated:
        if request.user.username == 'admin' or request.user.is_staff or request.user.is_superuser:
            return redirect('reports')
        else:
            return redirect('home')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect admin users to reports page, regular users to home
            if user.username == 'admin' or user.is_staff or user.is_superuser:
                return redirect('reports')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

@login_required
def home_view(request):
    # Redirect admin users to reports page
    if request.user.username == 'admin' or request.user.is_staff or request.user.is_superuser:
        return redirect('reports')

    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    context = {
        'user_team': profile.team_number,
        'has_team': profile.team_number is not None
    }
    return render(request, 'home.html', context)

@login_required
def get_available_teams(request):
    """Get list of teams that still have available slots"""
    team_status = UserProfile.get_team_status()
    available_teams = []

    for team_num, status in team_status.items():
        if not status['full']:
            available_teams.append({
                'number': team_num,
                'name': f'Team {team_num}',
                'current': status['current'],
                'capacity': status['capacity'],
                'available': status['available']
            })

    return JsonResponse({
        'available_teams': available_teams,
        'all_full': len(available_teams) == 0
    })

@login_required
@require_POST
def assign_team(request):
    try:
        data = json.loads(request.body)
        team_number = data.get('team_number')

        # Get or create user profile
        profile, created = UserProfile.objects.get_or_create(user=request.user)

        # Check if user already has a team
        if profile.team_number is not None:
            return JsonResponse({
                'success': False,
                'message': 'You are already assigned to a team',
                'team': profile.team_number
            })

        # Validate team number
        if team_number not in UserProfile.TEAM_CAPACITIES:
            return JsonResponse({
                'success': False,
                'message': 'Invalid team number',
                'team': None
            })

        # Check if the team has capacity
        team_status = UserProfile.get_team_status()
        if team_status[team_number]['full']:
            return JsonResponse({
                'success': False,
                'message': f'Team {team_number} is already full',
                'team': None
            })

        # Assign team
        profile.team_number = team_number
        profile.assigned_at = timezone.now()
        profile.save()

        return JsonResponse({
            'success': True,
            'message': f'Successfully assigned to Team {team_number}',
            'team': team_number
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)

@login_required
def reports_view(request):
    # Check if user is admin
    if not (request.user.username == 'admin' or request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('home')

    # Get all user profiles with their team assignments
    profiles = UserProfile.objects.select_related('user').all().order_by('team_number', 'user__username')

    # Group users by team
    teams = {}
    unassigned = []

    for profile in profiles:
        if profile.team_number:
            if profile.team_number not in teams:
                teams[profile.team_number] = []
            teams[profile.team_number].append(profile)
        else:
            unassigned.append(profile)

    # Get team capacities
    team_capacities = UserProfile.TEAM_CAPACITIES

    context = {
        'teams': dict(sorted(teams.items())),
        'unassigned': unassigned,
        'total_users': profiles.count(),
        'assigned_users': profiles.filter(team_number__isnull=False).count(),
        'unassigned_users': profiles.filter(team_number__isnull=True).count(),
        'team_capacities': team_capacities
    }

    return render(request, 'reports.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')
