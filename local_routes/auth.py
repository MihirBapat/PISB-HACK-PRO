from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from local_db import db
from local_models import User, Patient

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['user_role'] = user.role
            flash(f'Welcome back, {user.name}!', 'success')

            if user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif user.role == 'doctor':
                return redirect(url_for('doctor.dashboard'))
            return redirect(url_for('booking.my_appointments'))

        flash('Invalid email or password.', 'danger')

    return render_template('auth/login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        username = request.form.get('username', '').strip()
        phone = request.form.get('phone', '').strip()
        password = request.form.get('password', '')

        if not all([name, email, username, password]):
            flash('Please fill in all required fields.', 'danger')
            return render_template('auth/register.html')

        if User.query.filter_by(email=email).first():
            flash('An account with that email already exists.', 'danger')
            return render_template('auth/register.html')

        if User.query.filter_by(username=username).first():
            flash('That username is already taken.', 'danger')
            return render_template('auth/register.html')

        user = User(
            name=name,
            email=email,
            username=username,
            phone=phone,
            role='patient',
            password_hash=generate_password_hash(password),
        )
        db.session.add(user)
        db.session.commit()

        # Create an empty patient profile
        db.session.add(Patient(user_id=user.id))
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))
