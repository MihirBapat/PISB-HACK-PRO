"""Booking flow tests: slot selection, confirmation, and cancellation."""

from datetime import date, timedelta

from local_models import Appointment, TimeSlot


def test_booking_flow_pages_render(client, patient, clinic, doctor, slot, login):
    login('patient@test.com')

    resp = client.get('/book')
    assert resp.status_code == 200
    assert b'Test Clinic' in resp.data

    resp = client.get(f'/book/clinic/{clinic.id}')
    assert resp.status_code == 200
    assert b'Dr. Test' in resp.data

    resp = client.get(f'/book/doctor/{doctor.id}')
    assert resp.status_code == 200
    assert b'09:00' in resp.data


def test_confirm_booking_creates_appointment_and_consumes_slot(client, db, patient, slot, login):
    login('patient@test.com')

    resp = client.post('/book/confirm', data={'slot_id': slot.id, 'notes': 'Headache'})
    assert resp.status_code == 200
    assert b'Appointment Confirmed' in resp.data

    appt = Appointment.query.one()
    assert appt.patient_id == patient.id
    assert appt.status == 'scheduled'
    assert appt.notes == 'Headache'

    # The slot must no longer be bookable.
    assert db.session.get(TimeSlot, slot.id).is_available is False


def test_slot_cannot_be_double_booked(client, db, patient, doctor, slot, login):
    """A second booking of the same slot must be refused, not silently accepted."""
    login('patient@test.com')
    client.post('/book/confirm', data={'slot_id': slot.id, 'notes': ''})

    resp = client.post('/book/confirm', data={'slot_id': slot.id, 'notes': ''},
                       follow_redirects=True)
    assert b'just been taken' in resp.data
    # Still exactly one appointment.
    assert Appointment.query.count() == 1


def test_past_slots_are_not_offered(client, db, patient, doctor, login):
    past = TimeSlot(doctor_id=doctor.id, date=date.today() - timedelta(days=2),
                    start_time='09:00', end_time='10:00', is_available=True)
    future = TimeSlot(doctor_id=doctor.id, date=date.today() + timedelta(days=2),
                      start_time='11:00', end_time='12:00', is_available=True)
    db.session.add_all([past, future])
    db.session.commit()

    login('patient@test.com')
    resp = client.get(f'/book/doctor/{doctor.id}')
    assert b'11:00' in resp.data
    assert b'09:00' not in resp.data


def test_unavailable_slots_are_not_offered(client, db, patient, doctor, slot, login):
    slot.is_available = False
    db.session.commit()

    login('patient@test.com')
    resp = client.get(f'/book/doctor/{doctor.id}')
    assert b'09:00' not in resp.data


def test_my_appointments_lists_only_own_appointments(client, db, patient, doctor, slot, login):
    from tests.conftest import _make_user
    other = _make_user('other@test.com', 'other', 'Other Person', 'patient')
    db.session.add(Appointment(patient_id=other.id, doctor_id=doctor.id,
                               time_slot_id=slot.id, status='scheduled'))
    db.session.commit()

    login('patient@test.com')
    resp = client.get('/my-appointments')
    assert resp.status_code == 200
    assert b'no appointments yet' in resp.data.lower()


def test_cancel_releases_the_slot(client, db, patient, slot, login):
    login('patient@test.com')
    client.post('/book/confirm', data={'slot_id': slot.id, 'notes': ''})
    appt = Appointment.query.one()

    client.post(f'/appointment/{appt.id}/cancel')

    assert db.session.get(Appointment, appt.id).status == 'cancelled'
    assert db.session.get(TimeSlot, slot.id).is_available is True


def test_cannot_cancel_a_completed_appointment(client, db, patient, slot, login):
    """Cancelling a completed appointment must not free the slot back up."""
    login('patient@test.com')
    client.post('/book/confirm', data={'slot_id': slot.id, 'notes': ''})
    appt = Appointment.query.one()
    appt.status = 'completed'
    db.session.commit()

    resp = client.post(f'/appointment/{appt.id}/cancel', follow_redirects=True)
    assert b'already completed' in resp.data

    assert db.session.get(Appointment, appt.id).status == 'completed'
    assert db.session.get(TimeSlot, slot.id).is_available is False


def test_cannot_cancel_another_patients_appointment(client, db, patient, doctor, slot, login):
    from tests.conftest import _make_user
    victim = _make_user('victim@test.com', 'victim', 'Victim', 'patient')
    appt = Appointment(patient_id=victim.id, doctor_id=doctor.id,
                       time_slot_id=slot.id, status='scheduled')
    db.session.add(appt)
    slot.is_available = False
    db.session.commit()

    login('patient@test.com')
    resp = client.post(f'/appointment/{appt.id}/cancel', follow_redirects=True)
    assert b'cannot cancel' in resp.data.lower()
    assert db.session.get(Appointment, appt.id).status == 'scheduled'
