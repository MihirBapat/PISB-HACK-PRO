import os
import logging
from local_models import db, User, Patient, Clinic, Doctor, TimeSlot
from flask import Flask, render_template
from werkzeug.middleware.proxy_fix import ProxyFix
import logging
from local_db import db

# Create Flask app
app = Flask(__name__)

# Enable proxy support (useful if deployed behind reverse proxy)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Development logging setup
logging.basicConfig(level=logging.DEBUG)

# Secret key for sessions
app.secret_key = os.environ.get("SESSION_SECRET", "your-local-secret-key-for-development-only")

# Determine database URL (use SQLite for local development if not set)
database_url = os.environ.get("DATABASE_URL")
if not database_url or database_url.startswith("postgresql://"):
    database_url = "sqlite:///clinic_appointments.db"

# Configure SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize SQLAlchemy with app
db.init_app(app)

# Register blueprints
def register_blueprints():
    from local_routes.auth import auth_bp
    from local_routes.booking import booking_bp
    from local_routes.admin import admin_bp
    from local_routes.doctor import doctor_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(doctor_bp)

register_blueprints()

# Create default data inside app context
with app.app_context():
    import local_models
    db.create_all()

    from local_models import User, Clinic, Doctor, TimeSlot
    from werkzeug.security import generate_password_hash
    from datetime import datetime, timedelta

    # Admin setup
    if not User.query.filter_by(email='admin@clinic.com').first():
        admin_user = User(
            email='admin@clinic.com',
            name='System Administrator',
            username='admin',
            phone='555-0123',
            role='admin',
            password_hash=generate_password_hash('admin123')
        )
        db.session.add(admin_user)
        db.session.commit()
        print("✅ Default admin created: admin@clinic.com / admin123")

    # Clinic setup
    clinic = Clinic.query.filter_by(name='General Medical Center').first()
    if not clinic:
        clinic = Clinic(
            name='General Medical Center',
            address='123 Health Street, Medical City',
            phone='555-0100',
            email='info@generalmedical.com'
        )
        db.session.add(clinic)
        db.session.commit()
        print("🏥 Sample clinic created.")

    # Doctor setup
    doctor_user = User.query.filter_by(email='doctor@clinic.com').first()
    if not doctor_user:
        doctor_user = User(
            email='doctor@clinic.com',
            name='Dr. Sarah Johnson',
            username='drsarah',
            phone='555-0124',
            role='doctor',
            password_hash=generate_password_hash('doctor123')
        )
        db.session.add(doctor_user)
        db.session.commit()

    # Re-fetch user to ensure ID is available
    doctor_user = User.query.filter_by(email='doctor@clinic.com').first()

    # Now check and add doctor profile
    doctor_profile = Doctor.query.filter_by(user_id=doctor_user.id).first()
    if not doctor_profile:
        doctor_profile = Doctor(
            user_id=doctor_user.id,
            clinic_id=clinic.id,
            specialization='General Medicine',
            license_number='MD123456',
            years_experience=8
        )
        db.session.add(doctor_profile)
        db.session.commit()
        print("👩‍⚕️ Sample doctor created: doctor@clinic.com / doctor123")

        # Add time slots for next 7 days
        for day_offset in range(7):
            date = datetime.now().date() + timedelta(days=day_offset)
            for hour in range(9, 12):  # Morning
                db.session.add(TimeSlot(
                    doctor_id=doctor_profile.id,
                    date=date,
                    start_time=f"{hour:02d}:00",
                    end_time=f"{hour+1:02d}:00",
                    is_available=True
                ))
            for hour in range(14, 17):  # Afternoon
                db.session.add(TimeSlot(
                    doctor_id=doctor_profile.id,
                    date=date,
                    start_time=f"{hour:02d}:00",
                    end_time=f"{hour+1:02d}:00",
                    is_available=True
                ))
        db.session.commit()
        print("🕒 Sample time slots created for Dr. Sarah Johnson")

# Default route
@app.route('/')
def index():
    return render_template('index.html')

# Run locally
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
