# Local Development Setup Guide

## Quick Start Steps

### 1. Prerequisites Installation

**Required Software:**
- **Python 3.8+**: Download from [python.org](https://www.python.org/downloads/)
- **PostgreSQL**: Download from [postgresql.org](https://www.postgresql.org/download/)
- **VS Code**: Download from [code.visualstudio.com](https://code.visualstudio.com/)

### 2. Project Setup

```bash
# 1. Create project directory and navigate to it
mkdir multi-clinic-appointment-system
cd multi-clinic-appointment-system

# 2. Copy all project files to this directory
# (Copy all files from Replit to your local folder)

# 3. Create and activate virtual environment
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r local_requirements.txt
```

### 3. Database Setup

**Step 1: Install and Start PostgreSQL**
- Windows: Download installer from postgresql.org
- Mac: `brew install postgresql` then `brew services start postgresql`
- Linux: `sudo apt install postgresql postgresql-contrib`

**Step 2: Create Database**
```sql
-- Connect to PostgreSQL (usually with psql command)
CREATE DATABASE clinic_appointments;
CREATE USER clinic_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE clinic_appointments TO clinic_user;
```

**Step 3: Configure Environment**
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env file with your database credentials:
DATABASE_URL=postgresql://clinic_user:your_password@localhost:5432/clinic_appointments
SESSION_SECRET=your-very-long-secret-key-32-characters-minimum
```

### 4. VS Code Configuration

**Install Recommended Extensions:**
- Python (Microsoft)
- Python Debugger (Microsoft)
- GitLens (optional)

**Configure Python Interpreter:**
1. Open VS Code in project folder
2. Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (Mac)
3. Type "Python: Select Interpreter"
4. Choose the interpreter from your `venv` folder

### 5. Run the Application

```bash
# Method 1: Using the local main file
python local_main.py

# Method 2: Using VS Code debugger
# Press F5 or go to Run → Start Debugging
```

**Access the application at:** `http://localhost:5000`

### 6. Default Credentials

- **Admin Login**: admin@clinic.com / admin123
- **Patient**: Register through signup page
- **Doctor**: Created by admin through admin panel

## File Structure for Local Development

```
your-project-folder/
├── local_main.py          # Local development entry point
├── local_requirements.txt # Python dependencies
├── .env                   # Environment variables (create from .env.example)
├── .env.example          # Environment template
├── app.py                # Flask application setup
├── models.py             # Database models
├── routes/               # Application routes
├── templates/            # HTML templates  
├── static/               # CSS, JS, images
├── .vscode/              # VS Code configuration
│   ├── launch.json       # Debug configuration
│   └── settings.json     # Editor settings
└── README.md             # Full documentation
```

## Important Differences from Replit

### 1. Environment Variables
- **Replit**: Automatically managed
- **Local**: Use `.env` file (never commit this file!)

### 2. Database
- **Replit**: Managed PostgreSQL service
- **Local**: Install and configure PostgreSQL yourself

### 3. Port and Host
- **Replit**: Uses 0.0.0.0:5000 for external access
- **Local**: Uses 127.0.0.1:5000 for localhost only

### 4. Dependencies
- **Replit**: Managed through pyproject.toml
- **Local**: Use `local_requirements.txt` with pip

## Troubleshooting Common Issues

### Database Connection Errors
```bash
# Check if PostgreSQL is running
# Windows: Check Services or run `pg_ctl status`
# Mac/Linux: `brew services list` or `systemctl status postgresql`

# Test connection manually
psql -h localhost -U clinic_user -d clinic_appointments
```

### Port Already in Use
```bash
# Find what's using port 5000
# Windows: netstat -ano | findstr :5000
# Mac/Linux: lsof -i :5000

# Change port in .env file:
PORT=8000
```

### Virtual Environment Issues
```bash
# Deactivate and recreate if needed
deactivate
rm -rf venv  # or rmdir /s venv on Windows
python -m venv venv
# Reactivate and reinstall packages
```

### Module Import Errors
```bash
# Ensure virtual environment is activated
# You should see (venv) in your terminal prompt

# Reinstall packages if needed
pip install -r local_requirements.txt
```

## Development Workflow

1. **Always activate virtual environment first**
2. **Set up environment variables in .env**
3. **Run database migrations if needed**
4. **Start development server with hot reloading**
5. **Use VS Code debugger for troubleshooting**

## Next Steps

Once you have the application running locally:
1. Test all features (login, booking, admin panel)
2. Make your desired modifications
3. Consider version control with Git
4. Plan deployment strategy if needed

The local setup gives you full control over the development environment and allows for easy customization and debugging!