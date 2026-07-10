"""Shared pytest fixtures.

Every test runs against a fresh in-memory SQLite database, so tests are
isolated from each other and from the developer's clinic_appointments.db.
"""

import os
import sys
from datetime import date, timedelta

import pytest
from werkzeug.security import generate_password_hash

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from local_app import create_app
from local_db import db as _db
from local_models import User, Patient, Clinic, Doctor, TimeSlot


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': 'test-secret',
    })
    with app.app_context():
        _db.create_all()
        yield app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db(app):
    return _db


def _make_user(email, username, name, role, password='pass123'):
    user = User(
        email=email,
        username=username,
        name=name,
        role=role,
        password_hash=generate_password_hash(password),
    )
    _db.session.add(user)
    _db.session.commit()
    return user


@pytest.fixture
def admin(db):
    return _make_user('admin@test.com', 'admin', 'Admin User', 'admin')


@pytest.fixture
def patient(db):
    user = _make_user('patient@test.com', 'patient', 'Pat Patient', 'patient')
    db.session.add(Patient(user_id=user.id))
    db.session.commit()
    return user


@pytest.fixture
def clinic(db):
    c = Clinic(name='Test Clinic', address='1 Test Way', phone='555', email='c@t.com')
    db.session.add(c)
    db.session.commit()
    return c


@pytest.fixture
def doctor(db, clinic):
    user = _make_user('doc@test.com', 'doc', 'Dr. Test', 'doctor')
    d = Doctor(
        user_id=user.id,
        clinic_id=clinic.id,
        specialization='General Medicine',
        license_number='MD1',
        years_experience=5,
    )
    db.session.add(d)
    db.session.commit()
    return d


@pytest.fixture
def slot(db, doctor):
    s = TimeSlot(
        doctor_id=doctor.id,
        date=date.today() + timedelta(days=1),
        start_time='09:00',
        end_time='10:00',
        is_available=True,
    )
    db.session.add(s)
    db.session.commit()
    return s


@pytest.fixture
def login(client):
    """Log a user in by email/password and return the response."""
    def _login(email, password='pass123'):
        return client.post('/login', data={'email': email, 'password': password},
                           follow_redirects=False)
    return _login
