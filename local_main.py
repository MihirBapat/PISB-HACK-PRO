import os
from dotenv import load_dotenv
from flask_migrate import Migrate
from local_db import db 


# Load environment variables from .env file (optional for SQLite setup)
load_dotenv()

# Import the local app configuration
from local_app import app
migrate = Migrate(app, db)
if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    
    print("🏥 Multi-Clinic Appointment System")
    print("=" * 40)
    print(f"Server running at: http://127.0.0.1:{port}")
    print("Database: SQLite (clinic_appointments.db)")
    print("Default Admin: admin@clinic.com / admin123")
    print("Sample Doctor: doctor@clinic.com / doctor123")
    print("=" * 40)
    
    # Run the Flask development server
    app.run(
        host='127.0.0.1',  # localhost for local development
        port=port,
        debug=True
    )