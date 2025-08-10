from local_db import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    role = db.Column(db.String(20), nullable=False, default='patient')
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    appointments = db.relationship('Appointment', foreign_keys='Appointment.patient_id', backref='patient')
    doctor_profile = db.relationship('Doctor', backref='user', uselist=False)
    patient_profile = db.relationship('Patient', backref='user', uselist=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def full_name(self):
        return self.name

    def __repr__(self):
        return f'<User {self.email}>'

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    blood_group = db.Column(db.String(5))
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Patient {self.user.name} - {self.blood_group}>'

class Clinic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text, nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    doctors = db.relationship('Doctor', backref='clinic', lazy=True)

    def __repr__(self):
        return f'<Clinic {self.name}>'

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinic.id'), nullable=False)
    specialization = db.Column(db.String(100))
    license_number = db.Column(db.String(50))
    years_experience = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    time_slots = db.relationship('TimeSlot', backref='doctor', lazy=True)
    appointments = db.relationship('Appointment', foreign_keys='Appointment.doctor_id', backref='doctor')

    @property
    def name(self):
        return self.user.name if self.user else "Unknown"

    @property
    def email(self):
        return self.user.email if self.user else "Unknown"

    def __repr__(self):
        return f'<Doctor {self.name}>'

class TimeSlot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.String(10), nullable=False)
    end_time = db.Column(db.String(10), nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    appointments = db.relationship('Appointment', backref='time_slot', lazy=True)

    @property
    def formatted_time(self):
        return f"{self.start_time} - {self.end_time}"

    @property
    def clinic_name(self):
        return self.doctor.clinic.name if self.doctor and self.doctor.clinic else "Unknown"

    def __repr__(self):
        return f'<TimeSlot {self.date} {self.start_time}-{self.end_time}>'

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    time_slot_id = db.Column(db.Integer, db.ForeignKey('time_slot.id'), nullable=False)
    status = db.Column(db.String(20), default='scheduled')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def patient_name(self):
        return self.patient.name if self.patient else "Unknown"

    @property
    def doctor_name(self):
        return self.doctor.name if self.doctor else "Unknown"

    @property
    def clinic_name(self):
        return self.doctor.clinic.name if self.doctor and self.doctor.clinic else "Unknown"

    @property
    def appointment_date(self):
        return self.time_slot.date if self.time_slot else None

    @property
    def appointment_time(self):
        return self.time_slot.formatted_time if self.time_slot else "Unknown"

    def __repr__(self):
        return f'<Appointment {self.patient_name} with {self.doctor_name}>'
