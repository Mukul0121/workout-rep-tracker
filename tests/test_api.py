import os
import pytest
from app.server import create_app

@pytest.fixture
def client():
    test_db = 'data/test_api.db'
    if os.path.exists(test_db):
        os.remove(test_db)
    app = create_app(test_db)
    app.config.update({'TESTING': True})
    with app.test_client() as client:
        yield client
    if os.path.exists(test_db):
        os.remove(test_db)

def test_dashboard_route(client):
    response = client.get('/')
    assert response.status_code == 200

def test_create_and_list_sessions(client):
    # Test valid POST
    post_res = client.post('/api/sessions', json={'exercise': 'squat', 'reps': 10, 'duration_sec': 30})
    assert post_res.status_code == 201
    assert 'id' in post_res.get_json()

    # Test GET
    get_res = client.get('/api/sessions')
    assert get_res.status_code == 200
    assert len(get_res.get_json()) == 1

def test_invalid_input_returns_400(client):
    # Test bad exercise
    res1 = client.post('/api/sessions', json={'exercise': 'jumping_jacks', 'reps': 10, 'duration_sec': 30})
    assert res1.status_code == 400

    # Test negative reps
    res2 = client.post('/api/sessions', json={'exercise': 'squat', 'reps': -5, 'duration_sec': 30})
    assert res2.status_code == 400