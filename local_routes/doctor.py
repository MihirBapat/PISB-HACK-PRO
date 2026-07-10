from datetime import date, datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from local_db import db
from local_models import Doctor, TimeSlot, Appointment
from local_routes.utils import role_required, current_user

doctor_bp = Blueprint('doctor', __name__, url_prefix='/doctor')


def _current_doctor():
    user = current_user()
    if not user:
        return None
    return Doctor.query.filter_by(user_id=user.id).first()


@doctor_bp.route('/')
@role_required('doctor')
def dashboard():
    doctor = _current_doctor()
    if not doctor:
        flash('No doctor profile is linked to your account.', 'warning')
        return redirect(url_for('index'))

    upcoming = (Appointment.query
                .filter_by(doctor_id=doctor.id, status='scheduled')
                .all())
    stats = {
        'total_appointments': Appointment.query.filter_by(doctor_id=doctor.id).count(),
        'upcoming': len(upcoming),
        'slots': TimeSlot.query.filter_by(doctor_id=doctor.id).count(),
    }
    return render_template('doctor/dashboard.html', doctor=doctor, stats=stats)


@doctor_bp.route('/appointments')
@role_required('doctor')
def appointments():
    doctor = _current_doctor()
    if not doctor:
        return redirect(url_for('index'))
    appts = (Appointment.query
             .filter_by(doctor_id=doctor.id)
             .order_by(Appointment.created_at.desc())
             .all())
    return render_template('doctor/appointments.html', doctor=doctor, appointments=appts)


@doctor_bp.route('/schedule')
@role_required('doctor')
def schedule():
    doctor = _current_doctor()
    if not doctor:
        return redirect(url_for('index'))
    slots = (TimeSlot.query
             .filter_by(doctor_id=doctor.id)
             .order_by(TimeSlot.date, TimeSlot.start_time)
             .all())
    return render_template('doctor/schedule.html', doctor=doctor, slots=slots)


@doctor_bp.route('/schedule/add', methods=['POST'])
@role_required('doctor')
def add_slot():
    doctor = _current_doctor()
    if not doctor:
        return redirect(url_for('index'))

    slot_date = request.form.get('date', '')
    start_time = request.form.get('start_time', '')
    end_time = request.form.get('end_time', '')

    try:
        parsed_date = datetime.strptime(slot_date, '%Y-%m-%d').date()
    except ValueError:
        flash('Please provide a valid date.', 'danger')
        return redirect(url_for('doctor.schedule'))

    if not start_time or not end_time:
        flash('Start and end time are required.', 'danger')
        return redirect(url_for('doctor.schedule'))

    db.session.add(TimeSlot(
        doctor_id=doctor.id,
        date=parsed_date,
        start_time=start_time,
        end_time=end_time,
        is_available=True,
    ))
    db.session.commit()
    flash('Time slot added.', 'success')
    return redirect(url_for('doctor.schedule'))


@doctor_bp.route('/schedule/<int:slot_id>/delete', methods=['POST'])
@role_required('doctor')
def delete_slot(slot_id):
    slot = db.get_or_404(TimeSlot, slot_id)
    db.session.delete(slot)
    db.session.commit()
    flash('Time slot removed.', 'info')
    return redirect(url_for('doctor.schedule'))
