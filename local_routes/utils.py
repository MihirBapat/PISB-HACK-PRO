from functools import wraps
from flask import session, redirect, url_for, flash
from local_db import db
from local_models import User


def current_user():
    """Return the logged-in User object, or None."""
    user_id = session.get('user_id')
    if not user_id:
        return None
    return db.session.get(User, user_id)


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get('user_id'):
            flash('Please log in to continue.', 'warning')
            return redirect(url_for('auth.login'))
        return view(*args, **kwargs)
    return wrapped


def role_required(*roles):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not session.get('user_id'):
                flash('Please log in to continue.', 'warning')
                return redirect(url_for('auth.login'))
            if session.get('user_role') not in roles:
                flash('You do not have permission to access that page.', 'danger')
                return redirect(url_for('index'))
            return view(*args, **kwargs)
        return wrapped
    return decorator
