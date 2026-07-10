"""Authentication, registration and access-control tests."""

from local_models import User


def test_homepage_is_public(client):
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'ClinicCare' in resp.data


def test_register_creates_patient_account(client, db):
    resp = client.post('/register', data={
        'name': 'New User', 'email': 'new@test.com', 'username': 'newuser',
        'phone': '555-0000', 'password': 'secret123',
    })
    assert resp.status_code == 302

    user = User.query.filter_by(email='new@test.com').first()
    assert user is not None
    assert user.role == 'patient'
    # Password must never be stored in plaintext.
    assert user.password_hash != 'secret123'
    assert user.check_password('secret123')


def test_register_rejects_duplicate_email(client, patient):
    resp = client.post('/register', data={
        'name': 'Impostor', 'email': 'patient@test.com', 'username': 'other',
        'password': 'x', 'phone': '',
    })
    assert resp.status_code == 200
    assert b'already exists' in resp.data


def test_register_rejects_duplicate_username(client, patient):
    resp = client.post('/register', data={
        'name': 'Impostor', 'email': 'unique@test.com', 'username': 'patient',
        'password': 'x', 'phone': '',
    })
    assert resp.status_code == 200
    assert b'already taken' in resp.data


def test_login_with_valid_credentials(client, patient, login):
    resp = login('patient@test.com')
    assert resp.status_code == 302
    assert '/my-appointments' in resp.headers['Location']


def test_login_with_wrong_password_is_rejected(client, patient):
    resp = client.post('/login', data={'email': 'patient@test.com', 'password': 'wrong'})
    assert resp.status_code == 200
    assert b'Invalid email or password' in resp.data


def test_login_redirects_by_role(client, admin, doctor, login):
    assert '/admin/' in login('admin@test.com').headers['Location']
    client.get('/logout')
    assert '/doctor/' in login('doc@test.com').headers['Location']


def test_logout_clears_session(client, patient, login):
    login('patient@test.com')
    client.get('/logout')
    resp = client.get('/my-appointments')
    assert resp.status_code == 302
    assert '/login' in resp.headers['Location']


def test_anonymous_user_redirected_to_login(client):
    for path in ('/book', '/my-appointments', '/admin/', '/doctor/'):
        resp = client.get(path)
        assert resp.status_code == 302, path
        assert '/login' in resp.headers['Location'], path


def test_patient_cannot_access_admin_area(client, patient, login):
    login('patient@test.com')
    resp = client.get('/admin/')
    assert resp.status_code == 302
    assert '/admin' not in resp.headers['Location']


def test_patient_cannot_access_doctor_area(client, patient, login):
    login('patient@test.com')
    resp = client.get('/doctor/')
    assert resp.status_code == 302
    assert '/doctor' not in resp.headers['Location']


def test_doctor_cannot_access_admin_area(client, doctor, login):
    login('doc@test.com')
    resp = client.get('/admin/clinics')
    assert resp.status_code == 302


def test_404_page(client):
    resp = client.get('/no-such-page')
    assert resp.status_code == 404
    assert b'Page Not Found' in resp.data
