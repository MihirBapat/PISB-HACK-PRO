# Multi-Clinic Doctor Appointment System

A full-stack web application for managing doctor appointments across multiple clinics with role-based authentication and comprehensive booking management.

## Features

- **Role-based Authentication**: Patient, Doctor, and Admin roles
- **Complete Booking Flow**: Clinic selection → Doctor selection → Time slot booking
- **Admin Panel**: Full CRUD operations for clinics, doctors, appointments, and time slots
- **Doctor Dashboard**: Schedule management and appointment tracking
- **Patient Portal**: Registration, booking, and appointment history
- **Professional UI**: Medical-themed design with Bootstrap

## Local Development Setup

### Prerequisites

Before running this application locally, ensure you have the following installed:

1. **Python 3.8+** - [Download from python.org](https://www.python.org/downloads/)
2. **PostgreSQL** - [Download from postgresql.org](https://www.postgresql.org/download/)
3. **Git** - [Download from git-scm.com](https://git-scm.com/downloads/)
4. **VS Code** (recommended) - [Download from code.visualstudio.com](https://code.visualstudio.com/)

### Step 1: Clone and Setup Project

```bash
# Clone the repository (or download the files)
# Navigate to project directory
cd multi-clinic-appointment-system

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt
```

### Step 3: Database Setup (Two Options)

**Option A: SQLite (Recommended for Local Development)**
- No installation needed! SQLite comes with Python
- Database file (`clinic_appointments.db`) created automatically
- Perfect for development and testing

**Option B: PostgreSQL (Advanced)**
```sql
-- If you prefer PostgreSQL, create a database:
CREATE DATABASE clinic_appointments;
CREATE USER clinic_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE clinic_appointments TO clinic_user;
```

**Environment Configuration** (Optional):
Create a `.env` file only if you want to customize settings:
```env
# Optional: Only needed for custom configuration
SESSION_SECRET=your-secret-key-here-make-it-long-and-random
DATABASE_URL=postgresql://user:pass@localhost:5432/clinic_appointments  # Only for PostgreSQL
```

### Step 4: VS Code Configuration

1. **Install VS Code Extensions**:
   - Python
   - Python Debugger
   - SQLite Viewer (optional)
   - GitLens (optional)

2. **Configure VS Code Settings**:
   - Open Command Palette (Ctrl+Shift+P)
   - Select "Python: Select Interpreter"
   - Choose the interpreter from your virtual environment

### Step 5: Initialize Database

```bash
# Run the application once to create tables
python main.py
```

The application will automatically create all necessary tables and a default admin user.

### Step 6: Run the Application

```bash
# Start the Flask development server
python main.py
```

The application will be available at: `http://localhost:5000`

## Default Login Credentials

- **Admin**: admin@clinic.com / admin123
- **Patients**: Register through the signup page
- **Doctors**: Created by admins through the admin panel

## Project Structure

```
multi-clinic-appointment-system/
├── app.py              # Flask application setup
├── main.py             # Application entry point
├── models.py           # Database models
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (create this)
├── routes/            # Route blueprints
│   ├── auth.py        # Authentication routes
│   ├── booking.py     # Booking system routes
│   ├── admin.py       # Admin panel routes
│   └── doctor.py      # Doctor dashboard routes
├── templates/         # HTML templates
│   ├── base.html      # Base template
│   ├── auth/          # Authentication templates
│   ├── booking/       # Booking templates
│   ├── admin/         # Admin templates
│   └── doctor/        # Doctor templates
└── static/           # Static files
    ├── css/          # Stylesheets
    ├── js/           # JavaScript files
    └── images/       # Image assets
```

## Development Tips

1. **Database Reset**: If you need to reset the database, delete all tables and restart the application
2. **Environment Variables**: Never commit the `.env` file to version control
3. **Virtual Environment**: Always activate your virtual environment before working on the project
4. **Hot Reloading**: The Flask development server automatically reloads when you make changes

## Troubleshooting

### Common Issues:

1. **Port Already in Use**: Change the port in `main.py` if 5000 is occupied
2. **Database Connection**: Verify PostgreSQL is running and credentials are correct
3. **Module Not Found**: Ensure virtual environment is activated and dependencies are installed
4. **Permission Errors**: Check database user permissions

### VS Code Debugging:

Create `.vscode/launch.json`:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Flask App",
            "type": "python",
            "request": "launch",
            "program": "main.py",
            "console": "integratedTerminal",
            "env": {
                "FLASK_ENV": "development",
                "FLASK_DEBUG": "1"
            }
        }
    ]
}
```

## Production Deployment

For production deployment, consider:
- Using a production WSGI server (Gunicorn, uWSGI)
- Setting up a reverse proxy (Nginx)
- Using environment-specific configuration
- Setting up proper logging
- Implementing backup strategies

## Support

If you encounter any issues during setup, check:
1. Python version compatibility
2. PostgreSQL service status
3. Virtual environment activation
4. Environment variable configuration

Happy coding! 🏥