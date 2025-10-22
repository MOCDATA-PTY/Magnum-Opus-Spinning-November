# Team Spinner - November Edition

A Django-based team assignment application with an interactive spinning wheel.

## Features

- 🎡 **Interactive Spinning Wheel** - Users spin to get randomly assigned to teams
- 📊 **Team Capacity Management** - Teams 1-2 have 5 slots, Teams 3-6 have 6 slots
- 👥 **Admin Reports** - View all team assignments and user status
- 🎨 **Microsoft-Style UI** - Clean, professional light mode design
- 🔒 **User Authentication** - Secure login system

## Team Configuration

- **Team 1**: 5 members max
- **Team 2**: 5 members max
- **Team 3**: 5 members max
- **Team 4**: 6 members max
- **Team 5**: 6 members max
- **Team 6**: 6 members max
- **Total Capacity**: 33 users

## User Accounts

### Admin Account
- Username: `admin`
- Password: `admin123`
- Access: Reports page only

### Regular Users
- Username: `Anthony` | Password: `password`
- Username: `Johannes` | Password: `password`
- Username: `Jane` | Password: `password`
- Username: `Ethan` | Password: `password`

## Installation

1. Clone the repository:
```bash
git clone https://github.com/MOCDATA-PTY/Magnum-Opus-Spinning-November.git
cd Magnum-Opus-Spinning-November
```

2. Install dependencies:
```bash
pip install django
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Create admin user (if needed):
```bash
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver 0.0.0.0:8000
```

## Usage

### For Regular Users:
1. Navigate to `http://localhost:8000/`
2. Login with your credentials
3. Click the "SPIN" button
4. Get assigned to an available team
5. Team assignment is permanent

### For Admins:
1. Navigate to `http://localhost:8000/`
2. Login with admin credentials
3. View the reports page with all team assignments
4. See team capacities and user statuses

## How It Works

1. **Dynamic Team Loading**: The wheel only shows teams that have available slots
2. **Capacity Management**: When a team reaches capacity, it's removed from the wheel
3. **Fair Assignment**: Users land on a specific team and are assigned to that exact team
4. **One Spin Per User**: Each user can only spin once and cannot change teams

## Network Access

To make the application available on your local network:

```bash
python manage.py runserver 0.0.0.0:8000
```

Access from other devices: `http://YOUR_IP:8000/`

## Technologies Used

- **Backend**: Django 5.1.7
- **Frontend**: HTML5, CSS3, JavaScript
- **UI Framework**: Tailwind CSS
- **Database**: SQLite (default)

## Project Structure

```
Magnum-Opus-Spinning-November/
├── auth_app/              # Main application
│   ├── models.py          # UserProfile model with team logic
│   ├── views.py           # Login, home, reports views
│   ├── urls.py            # URL routing
│   └── admin.py           # Admin configuration
├── templates/             # HTML templates
│   ├── base.html          # Base template
│   ├── login.html         # Login page
│   ├── home.html          # Spinning wheel page
│   └── reports.html       # Admin reports page
├── magnum_opus/          # Project settings
│   ├── settings.py        # Django settings
│   └── urls.py            # Main URL configuration
└── manage.py              # Django management script
```

## License

This project is proprietary software owned by MOCDATA-PTY.

## Support

For issues or questions, please contact the development team.
