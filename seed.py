"""Idempotent database seeding for local development and demos.

Running this more than once is safe: every record is looked up before it is
created, so `python seed.py` can be re-run without duplicating data.
"""

from datetime import datetime, timedelta

from werkzeug.security import generate_password_hash

from local_db import db
from local_models import User, Patient, Clinic, Doctor, TimeSlot, Appointment

# --- Demo dataset -----------------------------------------------------------

CLINICS = [
    ('General Medical Center', '123 Health Street, Medical City', '555-0100', 'info@generalmedical.com'),
    ('Northside Family Clinic', '45 North Road, Riverside', '555-0200', 'contact@northside.com'),
    ('Lakeview Specialty Hospital', '9 Lakeview Avenue, Eastport', '555-0300', 'hello@lakeview.com'),
]

# (name, email, username, phone, clinic_index, specialization, license, years)
DOCTORS = [
    ('Dr. Sarah Johnson', 'doctor@clinic.com', 'drsarah', '555-0124', 0, 'General Medicine', 'MD123456', 8),
    ('Dr. Rajiv Menon', 'rajiv@clinic.com', 'drrajiv', '555-0125', 0, 'Cardiology', 'MD234567', 15),
    ('Dr. Emily Chen', 'emily@clinic.com', 'dremily', '555-0126', 1, 'Pediatrics', 'MD345678', 6),
    ('Dr. Marcus Webb', 'marcus@clinic.com', 'drmarcus', '555-0127', 2, 'Orthopaedics', 'MD456789', 20),
]

# (name, email, username, phone)
PATIENTS = [
    ('Priya Sharma', 'priya@example.com', 'priya', '555-1001'),
    ('Daniel Okafor', 'daniel@example.com', 'daniel', '555-1002'),
    ('Aisha Rahman', 'aisha@example.com', 'aisha', '555-1003'),
]

MORNING_HOURS = range(9, 12)
AFTERNOON_HOURS = range(14, 17)
SLOT_DAYS = 7


def _get_or_create_user(email, **kwargs):
    user = User.query.filter_by(email=email).first()
    if user:
        return user, False
    user = User(email=email, **kwargs)
    db.session.add(user)
    db.session.commit()
    return user, True


def seed_database(verbose=True):
    """Populate the database with a realistic demo dataset."""

    def log(message):
        if verbose:
            print(message)

    # --- Admin ---
    admin, created = _get_or_create_user(
        'admin@clinic.com',
        name='System Administrator',
        username='admin',
        phone='555-0123',
        role='admin',
        password_hash=generate_password_hash('admin123'),
    )
    if created:
        log('Admin created:   admin@clinic.com / admin123')

    # --- Clinics ---
    clinics = []
    for name, address, phone, email in CLINICS:
        clinic = Clinic.query.filter_by(name=name).first()
        if not clinic:
            clinic = Clinic(name=name, address=address, phone=phone, email=email)
            db.session.add(clinic)
            db.session.commit()
            log(f'Clinic created:  {name}')
        clinics.append(clinic)

    # --- Doctors (+ their time slots) ---
    doctors = []
    for name, email, username, phone, clinic_idx, spec, license_no, years in DOCTORS:
        user, _ = _get_or_create_user(
            email,
            name=name,
            username=username,
            phone=phone,
            role='doctor',
            password_hash=generate_password_hash('doctor123'),
        )

        doctor = Doctor.query.filter_by(user_id=user.id).first()
        if not doctor:
            doctor = Doctor(
                user_id=user.id,
                clinic_id=clinics[clinic_idx].id,
                specialization=spec,
                license_number=license_no,
                years_experience=years,
            )
            db.session.add(doctor)
            db.session.commit()
            log(f'Doctor created:  {name} ({spec})')

            today = datetime.now().date()
            for day_offset in range(SLOT_DAYS):
                slot_date = today + timedelta(days=day_offset)
                for hour in list(MORNING_HOURS) + list(AFTERNOON_HOURS):
                    db.session.add(TimeSlot(
                        doctor_id=doctor.id,
                        date=slot_date,
                        start_time=f'{hour:02d}:00',
                        end_time=f'{hour + 1:02d}:00',
                        is_available=True,
                    ))
            db.session.commit()
        doctors.append(doctor)

    # --- Patients ---
    patients = []
    for name, email, username, phone in PATIENTS:
        user, created = _get_or_create_user(
            email,
            name=name,
            username=username,
            phone=phone,
            role='patient',
            password_hash=generate_password_hash('patient123'),
        )
        if created:
            db.session.add(Patient(user_id=user.id))
            db.session.commit()
            log(f'Patient created: {name} / patient123')
        patients.append(user)

    # --- Appointments in a spread of states, so dashboards look real ---
    if Appointment.query.count() == 0:
        demo = [
            (patients[0], doctors[0], 'scheduled', 'Persistent headaches for two weeks.'),
            (patients[1], doctors[1], 'completed', 'Routine cardiac check-up.'),
            (patients[2], doctors[2], 'scheduled', 'Child has a recurring cough.'),
            (patients[0], doctors[3], 'cancelled', 'Knee pain after running.'),
        ]
        for patient, doctor, status, notes in demo:
            slot = (TimeSlot.query
                    .filter_by(doctor_id=doctor.id, is_available=True)
                    .order_by(TimeSlot.date, TimeSlot.start_time)
                    .first())
            if not slot:
                continue

            db.session.add(Appointment(
                patient_id=patient.id,
                doctor_id=doctor.id,
                time_slot_id=slot.id,
                status=status,
                notes=notes,
            ))
            # A cancelled appointment frees its slot again; the others hold it.
            slot.is_available = (status == 'cancelled')
        db.session.commit()
        log('Demo appointments created (scheduled / completed / cancelled)')


if __name__ == '__main__':
    from local_app import app

    with app.app_context():
        db.create_all()
        seed_database()
        print('\nDatabase seeded.')
