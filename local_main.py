"""Entry point for local development.

Creates the database schema, seeds demo data, and starts the Flask dev server.
"""

import os

from dotenv import load_dotenv
from flask_migrate import Migrate

load_dotenv()

from local_app import app
from local_db import db
from seed import seed_database

migrate = Migrate(app, db)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))

    with app.app_context():
        db.create_all()
        seed_database(verbose=True)

    print()
    print('🏥 Multi-Clinic Appointment System')
    print('=' * 44)
    print(f'Server running at: http://127.0.0.1:{port}')
    print('Database: SQLite (clinic_appointments.db)')
    print('Admin:   admin@clinic.com   / admin123')
    print('Doctor:  doctor@clinic.com  / doctor123')
    print('Patient: priya@example.com  / patient123')
    print('=' * 44)

    app.run(host='127.0.0.1', port=port, debug=True)
