from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
    path('reports/', views.reports_view, name='reports'),
    path('logout/', views.logout_view, name='logout'),
    path('get-available-teams/', views.get_available_teams, name='get_available_teams'),
    path('assign-team/', views.assign_team, name='assign_team'),
]
