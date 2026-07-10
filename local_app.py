"""Application factory and configuration for the Multi-Clinic Appointment System."""

import os
import sys
import logging

# Windows consoles default to cp1252, which cannot encode the emoji used in the
# startup banner. Force UTF-8 so those prints don't raise UnicodeEncodeError.
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from flask import Flask, render_template
from werkzeug.middleware.proxy_fix import ProxyFix

from local_db import db

# Imported for its side effect: registering the ORM mappers with `db` so that
# db.create_all() knows about every table.
import local_models  # noqa: F401


def _database_url():
    """Resolve the database URL, defaulting to local SQLite."""
    url = os.environ.get('DATABASE_URL')
    # The Replit deployment set a postgresql:// URL that is not reachable
    # locally, so fall back to SQLite unless a non-postgres URL is supplied.
    if not url or url.startswith('postgresql://'):
        return 'sqlite:///clinic_appointments.db'
    return url


def register_blueprints(app):
    from local_routes.auth import auth_bp
    from local_routes.booking import booking_bp
    from local_routes.admin import admin_bp
    from local_routes.doctor import doctor_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(doctor_bp)


def create_app(test_config=None):
    """Build and configure a Flask app.

    Passing ``test_config`` lets the test-suite swap in an isolated
    in-memory database without touching the developer's SQLite file.
    """
    app = Flask(__name__)

    # Trust proxy headers when deployed behind nginx / a platform router.
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    app.config['SECRET_KEY'] = os.environ.get(
        'SESSION_SECRET', 'your-local-secret-key-for-development-only'
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = _database_url()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # pool_recycle/pre_ping matter for server-side databases (Postgres) but are
    # meaningless for SQLite, which has no long-lived network connections.
    if not app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite'):
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
            'pool_recycle': 300,
            'pool_pre_ping': True,
        }

    if test_config:
        app.config.update(test_config)
    else:
        logging.basicConfig(level=logging.INFO)

    db.init_app(app)
    register_blueprints(app)

    @app.context_processor
    def inject_user():
        from local_routes.utils import current_user
        return {'current_user': current_user()}

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.errorhandler(404)
    def not_found(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    return app


# Module-level app so `from local_app import app` keeps working.
app = create_app()
