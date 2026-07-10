from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from local_db import db
from local_models import User, Clinic, Doctor, Appointment, TimeSlot
from local_routes.utils import role_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/')
@role_required('admin')
def dashboard():
    stats = {
        'clinics': Clinic.query.count(),
        'doctors': Doctor.query.count(),
        'patients': User.query.filter_by(role='patient').count(),
        'appointments': Appointment.query.count(),
    }
    recent = Appointment.query.order_by(Appointment.created_at.desc()).limit(10).all()
    return render_template('admin/dashboard.html', stats=stats, recent=recent)


# ---- Clinics ----
@admin_bp.route('/clinics')
@role_required('admin')
def manage_clinics():
    clinics = Clinic.query.order_by(Clinic.name).all()
    return render_template('admin/manage_clinics.html', clinics=clinics)


@admin_bp.route('/clinics/add', methods=['POST'])
@role_required('admin')
def add_clinic():
    clinic = Clinic(
        name=request.form.get('name', '').strip(),
        address=request.form.get('address', '').strip(),
        phone=request.form.get('phone', '').strip(),
        email=request.form.get('email', '').strip(),
    )
    if not clinic.name or not clinic.address:
        flash('Clinic name and address are required.', 'danger')
    else:
        db.session.add(clinic)
        db.session.commit()
        flash('Clinic added.', 'success')
    return redirect(url_for('admin.manage_clinics'))


@admin_bp.route('/clinics/<int:clinic_id>/delete', methods=['POST'])
@role_required('admin')
def delete_clinic(clinic_id):
    clinic = db.get_or_404(Clinic, clinic_id)
    db.session.delete(clinic)
    db.session.commit()
    flash('Clinic deleted.', 'info')
    return redirect(url_for('admin.manage_clinics'))


# ---- Doctors ----
@admin_bp.route('/doctors')
@role_required('admin')
def manage_doctors():
    doctors = Doctor.query.all()
    clinics = Clinic.query.order_by(Clinic.name).all()
    return render_template('admin/manage_doctors.html', doctors=doctors, clinics=clinics)


@admin_bp.route('/doctors/add', methods=['POST'])
@role_required('admin')
def add_doctor():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip().lower()
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    clinic_id = request.form.get('clinic_id', type=int)

    if not all([name, email, username, password, clinic_id]):
        flash('Please fill in all required fields.', 'danger')
        return redirect(url_for('admin.manage_doctors'))

    if User.query.filter((User.email == email) | (User.username == username)).first():
        flash('A user with that email or username already exists.', 'danger')
        return redirect(url_for('admin.manage_doctors'))

    user = User(
        name=name,
        email=email,
        username=username,
        phone=request.form.get('phone', '').strip(),
        role='doctor',
        password_hash=generate_password_hash(password),
    )
    db.session.add(user)
    db.session.commit()

    doctor = Doctor(
        user_id=user.id,
        clinic_id=clinic_id,
        specialization=request.form.get('specialization', '').strip(),
        license_number=request.form.get('license_number', '').strip(),
        years_experience=request.form.get('years_experience', type=int) or 0,
    )
    db.session.add(doctor)
    db.session.commit()
    flash('Doctor added.', 'success')
    return redirect(url_for('admin.manage_doctors'))


@admin_bp.route('/doctors/<int:doctor_id>/delete', methods=['POST'])
@role_required('admin')
def delete_doctor(doctor_id):
    doctor = db.get_or_404(Doctor, doctor_id)
    user = doctor.user
    db.session.delete(doctor)
    if user:
        db.session.delete(user)
    db.session.commit()
    flash('Doctor deleted.', 'info')
    return redirect(url_for('admin.manage_doctors'))


# ---- Appointments ----
@admin_bp.route('/appointments')
@role_required('admin')
def manage_appointments():
    appointments = Appointment.query.order_by(Appointment.created_at.desc()).all()
    return render_template('admin/manage_appointments.html', appointments=appointments)


@admin_bp.route('/appointments/<int:appointment_id>/status', methods=['POST'])
@role_required('admin')
def update_appointment_status(appointment_id):
    appointment = db.get_or_404(Appointment, appointment_id)
    new_status = request.form.get('status', 'scheduled')
    appointment.status = new_status
    if new_status == 'cancelled' and appointment.time_slot:
        appointment.time_slot.is_available = True
    db.session.commit()
    flash('Appointment updated.', 'success')
    return redirect(url_for('admin.manage_appointments'))
