"""Doctor dashboard and schedule-management tests."""

from datetime import date, timedelta

from local_models import Appointment, TimeSlot


def test_dashboard_shows_doctor_stats(client, db, doctor, patient, slot, login):
    db.session.add(Appointment(patient_id=patient.id, doctor_id=doctor.id,
                               time_slot_id=slot.id, status='scheduled'))
    db.session.commit()

    login('doc@test.com')
    resp = client.get('/doctor/')
    assert resp.status_code == 200
    assert b'Dr. Test' in resp.data
    assert b'General Medicine' in resp.data


def test_doctor_sees_own_appointments(client, db, doctor, patient, slot, login):
    db.session.add(Appointment(patient_id=patient.id, doctor_id=doctor.id,
                               time_slot_id=slot.id, status='scheduled',
                               notes='Migraine'))
    db.session.commit()

    login('doc@test.com')
    resp = client.get('/doctor/appointments')
    assert b'Pat Patient' in resp.data
    assert b'Migraine' in resp.data


def test_doctor_does_not_see_other_doctors_appointments(client, db, doctor, patient, clinic, login):
    from tests.conftest import _make_user
    from local_models import Doctor

    other_user = _make_user('other@doc.com', 'otherdoc', 'Dr. Other', 'doctor')
    other = Doctor(user_id=other_user.id, clinic_id=clinic.id, specialization='ENT')
    db.session.add(other)
    db.session.commit()

    other_slot = TimeSlot(doctor_id=other.id, date=date.today() + timedelta(days=1),
                          start_time='13:00', end_time='14:00', is_available=False)
    db.session.add(other_slot)
    db.session.commit()
    db.session.add(Appointment(patient_id=patient.id, doctor_id=other.id,
                               time_slot_id=other_slot.id, status='scheduled',
                               notes='Confidential'))
    db.session.commit()

    login('doc@test.com')
    resp = client.get('/doctor/appointments')
    assert b'Confidential' not in resp.data


def test_add_time_slot(client, db, doctor, login):
    login('doc@test.com')
    target = (date.today() + timedelta(days=3)).isoformat()
    client.post('/doctor/schedule/add', data={
        'date': target, 'start_time': '10:00', 'end_time': '11:00',
    })

    created = TimeSlot.query.filter_by(start_time='10:00').first()
    assert created is not None
    assert created.doctor_id == doctor.id
    assert created.is_available is True


def test_add_slot_rejects_invalid_date(client, db, doctor, login):
    login('doc@test.com')
    client.post('/doctor/schedule/add', data={
        'date': 'not-a-date', 'start_time': '10:00', 'end_time': '11:00',
    })
    assert TimeSlot.query.count() == 0


def test_delete_time_slot(client, db, doctor, slot, login):
    login('doc@test.com')
    client.post(f'/doctor/schedule/{slot.id}/delete')
    assert TimeSlot.query.count() == 0


def test_schedule_marks_booked_slots(client, db, doctor, patient, slot, login):
    slot.is_available = False
    db.session.add(Appointment(patient_id=patient.id, doctor_id=doctor.id,
                               time_slot_id=slot.id, status='scheduled'))
    db.session.commit()

    login('doc@test.com')
    resp = client.get('/doctor/schedule')
    assert b'>Booked<' in resp.data
