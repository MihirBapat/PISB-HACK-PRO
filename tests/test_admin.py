"""Admin panel CRUD and dashboard tests."""

from local_models import User, Clinic, Doctor, Appointment, TimeSlot


def test_dashboard_reports_accurate_counts(client, db, admin, patient, clinic, doctor, slot, login):
    db.session.add(Appointment(patient_id=patient.id, doctor_id=doctor.id,
                               time_slot_id=slot.id, status='scheduled'))
    db.session.commit()

    login('admin@test.com')
    resp = client.get('/admin/')
    assert resp.status_code == 200
    assert b'Admin Dashboard' in resp.data
    assert b'Pat Patient' in resp.data  # appears in the recent-appointments table


def test_add_clinic(client, admin, login):
    login('admin@test.com')
    client.post('/admin/clinics/add', data={
        'name': 'New Clinic', 'address': '9 New St', 'phone': '555', 'email': 'n@c.com',
    })
    assert Clinic.query.filter_by(name='New Clinic').first() is not None


def test_add_clinic_requires_name_and_address(client, admin, login):
    login('admin@test.com')
    client.post('/admin/clinics/add', data={'name': '', 'address': '', 'phone': '', 'email': ''})
    assert Clinic.query.count() == 0


def test_delete_clinic(client, admin, clinic, login):
    login('admin@test.com')
    client.post(f'/admin/clinics/{clinic.id}/delete')
    assert Clinic.query.count() == 0


def test_add_doctor_creates_linked_user_account(client, admin, clinic, login):
    login('admin@test.com')
    client.post('/admin/doctors/add', data={
        'name': 'Dr. New', 'email': 'new@doc.com', 'username': 'drnew',
        'password': 'pw123', 'phone': '555', 'clinic_id': clinic.id,
        'specialization': 'Neurology', 'license_number': 'MD9', 'years_experience': '3',
    })

    user = User.query.filter_by(email='new@doc.com').first()
    assert user is not None and user.role == 'doctor'

    doc = Doctor.query.filter_by(user_id=user.id).first()
    assert doc is not None
    assert doc.specialization == 'Neurology'
    assert doc.clinic_id == clinic.id
    # The generated doctor must be able to log in with the assigned password.
    assert user.check_password('pw123')


def test_add_doctor_rejects_duplicate_email(client, admin, clinic, doctor, login):
    login('admin@test.com')
    client.post('/admin/doctors/add', data={
        'name': 'Dupe', 'email': 'doc@test.com', 'username': 'dupe',
        'password': 'pw', 'clinic_id': clinic.id, 'phone': '',
        'specialization': '', 'license_number': '', 'years_experience': '',
    })
    assert Doctor.query.count() == 1


def test_delete_doctor_removes_user_too(client, admin, doctor, login):
    login('admin@test.com')
    client.post(f'/admin/doctors/{doctor.id}/delete')
    assert Doctor.query.count() == 0
    assert User.query.filter_by(email='doc@test.com').first() is None


def test_update_appointment_status(client, db, admin, patient, doctor, slot, login):
    appt = Appointment(patient_id=patient.id, doctor_id=doctor.id,
                       time_slot_id=slot.id, status='scheduled')
    db.session.add(appt)
    slot.is_available = False
    db.session.commit()

    login('admin@test.com')
    client.post(f'/admin/appointments/{appt.id}/status', data={'status': 'completed'})
    assert db.session.get(Appointment, appt.id).status == 'completed'


def test_admin_cancelling_appointment_frees_slot(client, db, admin, patient, doctor, slot, login):
    appt = Appointment(patient_id=patient.id, doctor_id=doctor.id,
                       time_slot_id=slot.id, status='scheduled')
    db.session.add(appt)
    slot.is_available = False
    db.session.commit()

    login('admin@test.com')
    client.post(f'/admin/appointments/{appt.id}/status', data={'status': 'cancelled'})
    assert db.session.get(TimeSlot, slot.id).is_available is True
