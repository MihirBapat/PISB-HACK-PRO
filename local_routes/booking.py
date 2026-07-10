from datetime import date
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from local_db import db
from local_models import Clinic, Doctor, TimeSlot, Appointment
from local_routes.utils import login_required

booking_bp = Blueprint('booking', __name__)


@booking_bp.route('/book')
@login_required
def select_clinic():
    clinics = Clinic.query.order_by(Clinic.name).all()
    return render_template('booking/select_clinic.html', clinics=clinics)


@booking_bp.route('/book/clinic/<int:clinic_id>')
@login_required
def select_doctor(clinic_id):
    clinic = db.get_or_404(Clinic, clinic_id)
    doctors = Doctor.query.filter_by(clinic_id=clinic_id).all()
    return render_template('booking/select_doctor.html', clinic=clinic, doctors=doctors)


@booking_bp.route('/book/doctor/<int:doctor_id>')
@login_required
def select_time(doctor_id):
    doctor = db.get_or_404(Doctor, doctor_id)
    slots = (TimeSlot.query
             .filter(TimeSlot.doctor_id == doctor_id,
                     TimeSlot.is_available.is_(True),
                     TimeSlot.date >= date.today())
             .order_by(TimeSlot.date, TimeSlot.start_time)
             .all())
    return render_template('booking/select_time.html', doctor=doctor, slots=slots)


@booking_bp.route('/book/confirm', methods=['POST'])
@login_required
def confirm():
    slot_id = request.form.get('slot_id', type=int)
    notes = request.form.get('notes', '').strip()

    slot = db.get_or_404(TimeSlot, slot_id)
    if not slot.is_available:
        flash('Sorry, that time slot has just been taken. Please choose another.', 'warning')
        return redirect(url_for('booking.select_time', doctor_id=slot.doctor_id))

    appointment = Appointment(
        patient_id=session['user_id'],
        doctor_id=slot.doctor_id,
        time_slot_id=slot.id,
        status='scheduled',
        notes=notes,
    )
    slot.is_available = False
    db.session.add(appointment)
    db.session.commit()

    return render_template('booking/confirmation.html', appointment=appointment)


@booking_bp.route('/my-appointments')
@login_required
def my_appointments():
    appointments = (Appointment.query
                    .filter_by(patient_id=session['user_id'])
                    .order_by(Appointment.created_at.desc())
                    .all())
    return render_template('booking/my_appointments.html', appointments=appointments)


@booking_bp.route('/appointment/<int:appointment_id>/cancel', methods=['POST'])
@login_required
def cancel(appointment_id):
    appointment = db.get_or_404(Appointment, appointment_id)
    if appointment.patient_id != session['user_id']:
        flash('You cannot cancel that appointment.', 'danger')
        return redirect(url_for('booking.my_appointments'))

    if appointment.status != 'scheduled':
        flash(f'That appointment is already {appointment.status}.', 'warning')
        return redirect(url_for('booking.my_appointments'))

    appointment.status = 'cancelled'
    if appointment.time_slot:
        appointment.time_slot.is_available = True
    db.session.commit()
    flash('Appointment cancelled.', 'info')
    return redirect(url_for('booking.my_appointments'))
