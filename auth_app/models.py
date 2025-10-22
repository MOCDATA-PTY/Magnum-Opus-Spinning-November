from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    team_number = models.IntegerField(null=True, blank=True)
    assigned_at = models.DateTimeField(null=True, blank=True)

    # Team capacities: Teams 1-3 have 5 slots, Teams 4-6 have 6 slots
    TEAM_CAPACITIES = {
        1: 5,
        2: 5,
        3: 5,
        4: 6,
        5: 6,
        6: 6
    }

    def __str__(self):
        return f"{self.user.username} - Team {self.team_number if self.team_number else 'Unassigned'}"

    @classmethod
    def get_next_available_team(cls):
        """Get the next team that has available slots"""
        for team_num in cls.TEAM_CAPACITIES.keys():
            capacity = cls.TEAM_CAPACITIES[team_num]
            current_count = cls.objects.filter(team_number=team_num).count()

            if current_count < capacity:
                return team_num

        # If all teams are full, return None
        return None

    @classmethod
    def get_team_status(cls):
        """Get status of all teams with current count and capacity"""
        status = {}
        for team_num in cls.TEAM_CAPACITIES.keys():
            capacity = cls.TEAM_CAPACITIES[team_num]
            current_count = cls.objects.filter(team_number=team_num).count()
            status[team_num] = {
                'current': current_count,
                'capacity': capacity,
                'available': capacity - current_count,
                'full': current_count >= capacity
            }
        return status
