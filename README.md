# Multi-Clinic Doctor Appointment System

A Flask web application for booking doctor appointments across multiple clinics,
with role-based access control for patients, doctors, and administrators.

Built with Flask, SQLAlchemy, and Bootstrap. Covered by a 38-test pytest suite.

---

## Features

**Patients** register, browse clinics and doctors, book an available time slot in a
three-step flow, and view or cancel their appointments.

**Doctors** get a dashboard of their appointment load, see the patients booked with
them (and only them), and manage their own availability by adding or removing time slots.

**Administrators** get a system-wide dashboard and full CRUD over clinics, doctors,
and appointment statuses. Creating a doctor provisions their login account in the
same operation.

---

## Quick Start

```bash
# 1. Create and activate a virtual environment
python -m venv venv
 venv/Scripts/activate       # Windows
source venv/bin/activate     # macOS / Linux

# 2. Install dependencies
pip install -r local_requirements.txt

# 3. Run — creates the SQLite schema and seeds demo data on first launch
python local_main.py
```

Open **http://127.0.0.1:5000**.

No database server is required: the app defaults to SQLite and creates
`instance/clinic_appointments.db` automatically.

### Demo accounts

| Role    | Email                | Password     |
|---------|----------------------|--------------|
| Admin   | `admin@clinic.com`   | `admin123`   |
| Doctor  | `doctor@clinic.com`  | `doctor123`  |
| Patient | `priya@example.com`  | `patient123` |

Patients can also self-register at `/register`.

To reset the database, delete `instance/clinic_appointments.db` and re-run
`python local_main.py`, or re-seed in place with `python seed.py` (idempotent).

---

## Running the Tests

```bash
pip install pytest
pytest
```

38 tests run against an isolated in-memory SQLite database, so they never touch
your development data. Coverage includes:

- **Authentication** — registration, duplicate email/username rejection,
  password hashing, role-based login redirects, logout.
- **Access control** — anonymous users are redirected to login; patients cannot
  reach the admin or doctor areas; doctors cannot reach the admin area.
- **Booking** — the full clinic → doctor → slot flow, slot consumption,
  double-booking rejection, and exclusion of past/unavailable slots.
- **Data isolation** — patients see only their own appointments; doctors see only
  appointments booked with them.
- **Admin CRUD** — clinic and doctor creation/deletion, status transitions.

---

## Architecture

```
local_main.py          Entry point: creates schema, seeds data, runs the dev server
local_app.py           Application factory (create_app) + configuration
local_db.py            SQLAlchemy instance, shared to avoid circular imports
local_models.py        ORM models: User, Patient, Clinic, Doctor, TimeSlot, Appointment
seed.py                Idempotent demo-data seeding
local_routes/
    utils.py           current_user helper, @login_required / @role_required decorators
    auth.py            Registration, login, logout
    booking.py         Three-step booking flow and cancellation
    admin.py           Admin dashboard and CRUD
    doctor.py          Doctor dashboard and schedule management
templates/             Jinja2 templates (base layout + per-blueprint folders)
tests/                 pytest suite with fixtures for each role
```

### Data model

A `User` carries the `role` discriminator (`patient` / `doctor` / `admin`) and the
password hash. `Doctor` and `Patient` are profile tables hanging off `User`, so a
doctor is a user with a doctor profile rather than a separate identity.

A `TimeSlot` belongs to a doctor and carries an `is_available` flag. An
`Appointment` joins a patient, a doctor, and exactly one time slot.

---

## Engineering Notes

**Application factory.** `create_app(test_config=None)` lets the test suite build an
app bound to an in-memory database rather than the developer's SQLite file. Without
this, tests would mutate real data and could not run in isolation.

**Circular imports.** The SQLAlchemy `db` object lives alone in `local_db.py`. If it
were defined in `local_app.py`, the models would import the app and the app would
import the models. Isolating `db` breaks the cycle.

**Slot availability is authoritative.** `is_available` on `TimeSlot` is the single
source of truth for whether a slot can be booked. Booking sets it to `False`;
cancelling sets it back to `True`. `/book/confirm` re-checks the flag before writing,
so a slot taken between page load and submission is rejected rather than
double-booked.

**Cancellation is state-guarded.** Only a `scheduled` appointment can be cancelled.
An earlier version enforced this only by hiding the button in the template — the
route itself would happily cancel a *completed* appointment and wrongly return its
slot to the pool. Authorization and state checks belong in the route, not the view.
`test_cannot_cancel_a_completed_appointment` pins this.

**Ownership checks.** Cancelling verifies the appointment belongs to the session
user, so a patient cannot cancel someone else's appointment by guessing an ID.

**Timezone-aware timestamps.** `created_at` defaults use
`datetime.now(timezone.utc)`; `datetime.utcnow()` is deprecated in Python 3.12+.

---

## Known Limitations

Honest notes on what this does *not* do yet:

- **No CSRF protection.** State-changing forms should use Flask-WTF tokens before
  this is exposed to real users.
- **Slot booking is not transactionally locked.** The `is_available` re-check
  narrows the double-booking window but does not close it. Two simultaneous requests
  could both pass the check. A `SELECT ... FOR UPDATE` (or a unique constraint on
  `time_slot_id` for active appointments) would make it airtight.
- **No password strength requirements** and no rate limiting on login.
- **The dev server is not production-ready.** Deploy behind Gunicorn + a reverse
  proxy, set `SESSION_SECRET`, and switch `DATABASE_URL` to PostgreSQL.

---

## Configuration

All optional — the app runs with zero configuration.

| Variable         | Default                          | Purpose                          |
|------------------|----------------------------------|----------------------------------|
| `SESSION_SECRET` | a development placeholder        | Flask session signing key        |
| `DATABASE_URL`   | `sqlite:///clinic_appointments.db` | Database connection string     |
| `PORT`           | `5000`                           | Port for the development server  |

Set them in a `.env` file (see `.env.example`); it is loaded via `python-dotenv`.

> **Note:** `DATABASE_URL` values beginning with `postgresql://` are intentionally
> ignored in favour of SQLite, a carry-over from the project's original hosted
> environment. Remove that branch in `local_app._database_url()` to use PostgreSQL.
